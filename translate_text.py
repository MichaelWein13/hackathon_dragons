from googletrans import Translator

def translate_text(text: str, src_lang: str, dest_lang: str="en") -> str:
    """
    Translate text from source language to destination language using googletrans.

    Parameters:
        text (str): The text to translate.
        src_lang (str): The source language code (e.g., 'fr' for French, 'auto' for auto-detect).
        dest_lang (str): The destination language code (e.g., 'en' for English).

    Returns:
        str: The translated text.
    """
    try:
        translator = Translator()
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception as e:
        return f"Translation failed: {e}"

def main():
    # Example usage
    text_to_translate = "Bonjour tout le monde"
    source_language = "fr"  # French
    destination_language = "en"  # English

    translated_text = translate_text(text_to_translate, source_language, destination_language)
    print(f"Original: {text_to_translate}")
    print(f"Translated: {translated_text}")

if __name__ == '__main__':
    main()