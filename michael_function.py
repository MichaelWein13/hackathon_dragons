from openai import OpenAI
import requests
import json
import trafilatura
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

# Exa API settings
EXA_SEARCH_URL = "https://api.exa.ai/search"
REPUTABLE_DOMAINS = [
    "ncbi.nlm.nih.gov",  # National Institutes of Health
    "harvard.edu",  # Harvard University
    "nih.gov",  # National Institutes of Health
    "mayoclinic.org",  # Mayo Clinic
    "nature.com",  # Nature Publishing Group
    "sciencedirect.com",  # Elsevier ScienceDirect
    "who.int",  # World Health Organization
    "webmd.com",  # WebMD
    "bmj.com",  # British Medical Journal
    "thelancet.com",  # The Lancet
    "jamanetwork.com",  # JAMA Network
    "pubmed.ncbi.nlm.nih.gov",  # PubMed
    "cdc.gov",  # Centers for Disease Control and Prevention
    "americanheart.org",  # American Heart Association
    "adage.com",  # Advertising Age
    "reuters.com",  # Reuters News
    "bbc.com",  # BBC News
    "nytimes.com",  # New York Times
    "guardian.co.uk",  # The Guardian
    "forbes.com",  # Forbes
    "ft.com",  # Financial Times
    "wsj.com",  # The Wall Street Journal
    "scientificamerican.com",  # Scientific American
    "livescience.com",  # LiveScience
    "edu",  # General Education domains (.edu)
    "gov",  # Government domains (.gov)
]

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {EXA_API_KEY}"
}


def check_if_summary(text):
    """
    Check if the provided text seems like a summary of an article or something else.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text seems like a summary, False otherwise.
    """
    prompt = f"""
    You are given a text. Determine if the text seems remotely like a valid summary of an article or something else (e.g. telling you you can't access the webpage, telling you an email doesn't work).
    Respond with 'valid_summary' if it seems like a summary or 'not_summary' if it does not seem like a summary.

    Text:
    "{text}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        result = response.choices[0].message.content.strip().lower()
        return result == 'valid_summary'

    except Exception as e:
        print(f"Error checking summary: {e}")
        return False


def fetch_and_summarize(url):
    """
    Fetches a webpage, extracts its main content, and summarizes it using GPT.
    Returns "Summary invalid - hello!" if the page isn't suitable for summarizing.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        article_text = trafilatura.extract(response.text)

        if not article_text or len(article_text.strip()) < 100:
            return "Summary invalid"

        # Ask GPT to summarize
        prompt = f"""
You are a helpful assistant. Summarize the following article in 3-4 sentences. 
Do NOT ask a question. Only give a plain summary.

Article:
\"\"\"
{article_text.strip()}
\"\"\"
"""
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        summary = completion.choices[0].message.content.strip()

        # Check if the response is a valid summary
        if not check_if_summary(summary):
            # print("hey2: detected invalid summary")
            return "Summary invalid"

        return summary

    except Exception as e:
        # print(f"hey3: error during fetch/summarize - {e}")
        return "Summary invalid"


def extract_claims(raw_contradiction):
    prompt = f"""
You will be given a contradiction found in two texts. Extract and rephrase both sides as separate research questions suitable for web search.

Contradiction:
{raw_contradiction}

Return the result as JSON like:
{{
  "claim_1": "...",
  "claim_2": "..."
}}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return json.loads(response.choices[0].message.content)


def search_exa(query, num_results=8):
    payload = {
        "query": query,
        "num_results": num_results
    }

    response = requests.post(EXA_SEARCH_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    results = response.json().get("results", [])

    filtered = []
    for r in results:
        if any(domain in r["url"] for domain in REPUTABLE_DOMAINS):
            try:
                summary = fetch_and_summarize(r["url"])
                if summary == "Summary invalid":
                    continue  # Skip this result if summary is unavailable
                r["summary"] = summary
                filtered.append({
                    "title": r["title"],
                    "url": r["url"],
                    "domain": r["url"].split("/")[2],
                    "summary": r["summary"]
                })
            except Exception as e:
                r["summary"] = f"Summary unavailable. Error: {str(e)}"
                continue  # Skip this result in case of error
    return filtered


def investigate_contradiction(contradiction_list):
    results = []

    for contradiction_text in contradiction_list:
        # print(f"Extracting claims from contradiction: {contradiction_text}")

        # Extract the claims from the contradiction text
        claims = extract_claims(contradiction_text)

        # print(f"Searching for: {claims['claim_1']}")
        results1 = search_exa(claims["claim_1"])

        # print(f"Searching for: {claims['claim_2']}")
        results2 = search_exa(claims["claim_2"])

        results.append({
            "claim_1": {
                "text": claims["claim_1"],
                "sources": results1
            },
            "claim_2": {
                "text": claims["claim_2"],
                "sources": results2
            }
        })

    return results


# === Example test ===
if __name__ == "__main__":
    contradiction_input = [
        '- Contradiction: The claim about the D-Notice.\n  - Text 1: "The producers allege that the story was prevented from being told in 1971 because of a D-Notice, to protect a prominent member of the British royal family."\n  - Text 2: "There have been several rumours connected with the burglary, including one that the government issued a D-Notice to censor the press... There is no evidence to support these claims and they have been widely dismissed."',
        '- Contradiction: The claim about the film\'s inspiration.\n  - Text 1: "According to the producers, this film is intended to reveal the truth for the first time, although it apparently includes significant elements of fiction."\n  - Text 2: "Some of the rumours inspired the story for the 2008 film The Bank Job."'
    ]

    results = investigate_contradiction(contradiction_input)
    print(json.dumps(results, indent=2))
