from contradiction_detection.detector import ContradictionDetector

# Replace with your actual OpenAI API key
API_KEY = "your_key"

# Define the reference language
reference_language = "En"

# Define the dictionary of article texts in English (already translated)
text_dict = {
    "En": "The war began in 1947 and lasted for 2 years. The treaty was signed in 1949.",
    "Fr": "The war began in 1947 and lasted for 4 years. The treaty was signed in 1951.",
    "Es": "The war began in 1947 and lasted for 2 years. The treaty was signed in 1949.",
    "De": "The conflict started in 1946 and lasted 3 years. The treaty was finalized in 1949."
}

# Define the dictionary of URLs for each language version of the article
url_dict = {
    "En": "https://en.wikipedia.org/wiki/Example_Article",
    "Fr": "https://fr.wikipedia.org/wiki/Exemple_Article",
    "Es": "https://es.wikipedia.org/wiki/Ejemplo_Articulo",
    "De": "https://de.wikipedia.org/wiki/Beispiel_Artikel"
}

# Instantiate your contradiction detector
detector = ContradictionDetector(api_key=API_KEY)

# Run contradiction detection
contradictions = detector.detect_against_many(reference_language, text_dict, url_dict)

print(contradictions)
