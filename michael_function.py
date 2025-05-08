from openai import OpenAI
import requests
import json
import trafilatura

OPENAI_API_KEY = "PLACE_API_KEY"  # Your actual key
EXA_API_KEY = "PLACE_API_KEY"  # Your actual key

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
        response = requests.get(url, timeout=0.1)
        response.raise_for_status()
        article_text = trafilatura.extract(response.text)

        if not article_text or len(article_text.strip()) < 100:
            print('hey237593')
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

         #Check if the response is a valid summary
        if not check_if_summary(summary):
            print("hey2: detected invalid summary")
            return "Summary invalid"

        return summary

    except Exception as e:
        #print(f"hey3: error during fetch/summarize - {e}")
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
    try:
        claims = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        claims = None  # Or handle accordingly
    return claims


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
                # Try to fetch a summary
                summary = fetch_and_summarize(r["url"])

                # Add the article even if the summary is invalid
                if summary == "Summary invalid":
                    r["summary"] = "No summary available"
                else:
                    r["summary"] = summary

                # Append the article with or without a summary
                filtered.append({
                    "title": r["title"],
                    "url": r["url"],
                    "domain": r["url"].split("/")[2],
                    "summary": r["summary"]
                })

            except Exception:
                # In case of error, add the article with a message
                filtered.append({
                    "title": r["title"],
                    "url": r["url"],
                    "domain": r["url"].split("/")[2],
                    "summary": "Error fetching summary"
                })
    return filtered


def investigate_contradiction(contradiction_list):
    all_articles = []
    seen_articles = set()  # To store unique article identifiers (e.g., URLs)

    for contradiction_item in contradiction_list:
        language_code = contradiction_item[0]  # 'Fr' or 'De'
        url = contradiction_item[1]  # URL of the article
        contradiction_text = contradiction_item[2]  # Contradiction description
        text1_and_2 = contradiction_item[3].split('\n')  # Split the two texts

        if len(text1_and_2) < 2:
            continue  # Skip if there aren't two texts to compare

        # Extract the two texts
        text_1 = text1_and_2[0].replace("- Text 1: ", "").strip()
        text_2 = text1_and_2[1].replace("- Text 2: ", "").strip()

        # Extract claims for further investigation
        claims = extract_claims(f"Contradiction: {contradiction_text} - Text 1: {text_1} - Text 2: {text_2}")
        if not claims:
            continue

        # Search for articles
        articles_1 = search_exa(claims["claim_1"])
        articles_2 = search_exa(claims["claim_2"])

        # Combine and filter articles by uniqueness for each contradiction
        contradiction_results = []

        for article in articles_1 + articles_2:
            article_id = article.get("url") or article.get("id")  # use a unique key
            if article_id and article_id not in seen_articles:
                seen_articles.add(article_id)
                article["contradiction"] = contradiction_text  # Add contradiction context
                contradiction_results.append(article)

        all_articles.append(contradiction_results)

    return all_articles


# === Example test ===
if __name__ == "__main__":
    contradiction_input = [['Fr', 'https://fr.wikipedia.org/wiki/Exemple_Article', '- Contradiction: Duration of the war.', '- Text 1: "The war began in 1947 and lasted for 2 years."\n  - Text 2: "The war began in 1947 and lasted for 4 years."'], ['Fr', 'https://fr.wikipedia.org/wiki/Exemple_Article', '- Contradiction: Year the treaty was signed.', '- Text 1: "The treaty was signed in 1949."\n  - Text 2: "The treaty was signed in 1951."'], ['De', 'https://de.wikipedia.org/wiki/Beispiel_Artikel', '- Contradiction: The start year of the war.', '- Text 1: "The war began in 1947"\n  - Text 2: "The conflict started in 1946"'], ['De', 'https://de.wikipedia.org/wiki/Beispiel_Artikel', '- Contradiction: The duration of the war.', '- Text 1: "lasted for 2 years"\n  - Text 2: "lasted 3 years"']]

    results = investigate_contradiction(contradiction_input)
    print(results)
    print(json.dumps(results, indent=2))
