import openai
from concurrent.futures import ThreadPoolExecutor


# Input is a tuple of the form (str, dict1, dict2), where str is the name of the language which we compare all others with, 
# and dict1 is a dictionary of the form (language, text), and dict2 is of the form (language, url)
# Output is a list of contradictions, where each is in the form [language, url, brief description, fuller description]


class ContradictionDetector:
    def __init__(self, api_key):
        openai.api_key = api_key

    def detect_pair(self, text1, text2):
        prompt = f"""
You are a contradiction detection tool.

Compare the following two texts. Identify any **explicit contradictions between them.

⚠️ For each contradiction, write only the following:
- Writes a title for the contradiction.
- Quotes the **exact conflicting sentences or phrases** from each text using quotation marks.
- Separate every distinct contradiction by "***"
- Do not add anything else, including not adding any descriptions like 'for each contradiction' or 'Clearly state the contradiction'

❌ Do NOT paraphrase — only use direct quotes.
✅ If no contradictions are found, respond with: "No contradictions found."

For example
['- Contradiction: The claim about the D-Notice.\n  - Text 1: "The producers allege that the story was prevented from being told in 1971 because of a D-Notice, to protect a prominent member of the British royal family."\n  - Text 2: "There have been several rumours connected with the burglary, including one that the government issued a D-Notice to censor the press... There is no evidence to support these claims and they have been widely dismissed."'
 '- Contradiction: The claim about the film\'s inspiration.\n  - Text 1: "According to the producers, this film is intended to reveal the truth for the first time, although it apparently includes significant elements of fiction."\n  - Text 2: "Some of the rumours inspired the story for the 2008 film The Bank Job."']
Text 1:
{text1.strip()}

Text 2:
{text2.strip()}
"""
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    def detect_against_many(self, reference_language, text_dict, url_dict, max_workers=5):
        reference_text = text_dict[reference_language]
        comparison_items = [(lang, text) for lang, text in text_dict.items() if lang != reference_language]

        def process(lang, text):
            result = self.detect_pair(reference_text, text)
            if result.strip() == "No contradictions found.":
                return None
            # Split into individual contradictions
            contradictions = result.split("***")
            summaries = []
            for contradiction in contradictions:
                lines = contradiction.strip().split("\n")
                if len(lines) >= 2:
                    brief = lines[0].strip()
                    full = "\n".join(lines[1:]).strip()
                    summaries.append([lang, url_dict[lang], brief, full])
            return summaries

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(lambda item: process(*item), comparison_items)

        # Flatten and filter out None
        contradictions_list = [contradiction for sublist in results if sublist for contradiction in sublist]
        return contradictions_list
