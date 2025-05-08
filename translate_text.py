from google.cloud import translate_v2 as translate
import os

# Set the path to your downloaded service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "boxwood-airship-459214-i7-ccdaf9e33f21.json"

translate_client = translate.Client()

def translate_text(text: str, src_lang: str, dest_lang: str = "en") -> str:
    try:
        result = translate_client.translate(
            text,
            source_language=src_lang,
            target_language=dest_lang,
            format_='text'
        )
        return result["translatedText"]
    except Exception as e:
        return f"Translation failed: {e}"

def main():
    text_to_translate = "שלום עולם"
    source_language = "he"
    destination_language = "en"

    translated_text = translate_text(text_to_translate, source_language, destination_language)
    print(f"Original: {text_to_translate}")
    print(f"Translated: {translated_text}")

if __name__ == '__main__':
    main()
