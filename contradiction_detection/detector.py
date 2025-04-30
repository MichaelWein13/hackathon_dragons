import openai

class ContradictionDetector:
    def __init__(self, api_key):
        openai.api_key = api_key

    def detect(self, text1, text2):
        prompt = f"""
You are a contradiction detection tool.

Compare the following two texts. Identify any **explicit contradictions** between them.

⚠️ For each contradiction:
- Clearly state the contradiction.
- Quote the **exact conflicting sentences or phrases** from each text using quotation marks.

❌ Do NOT paraphrase — only use direct quotes.
✅ If no contradictions are found, respond with: "No contradictions found."

Text 1:
{text1.strip()}

Text 2:
{text2.strip()}
"""
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
