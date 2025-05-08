import time

from deep_translator import GoogleTranslator

# {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
def translate_text(text: str, src_lang: str, dest_lang: str = "en") -> str:
    if src_lang == "he":
        src_lang = "iw"
    if dest_lang == "he":
        dest_lang = "iw"

    # use the _translate_text, if returns error then wait 5 seconds and try again (try again up to 5 times)
    # if it fails, return None
    for sleep_time in [5, 10, 20, 1]:
        try:
            translated_text = _translate_text(text, src_lang, dest_lang)
            return translated_text
        except Exception as e:
            print(f"Translation failed: ({src_lang}) {e}")
            # wait 5 seconds
            time.sleep(sleep_time)


def _translate_text(text: str, src_lang: str, dest_lang: str = "en") -> str:
    """
    Translate text from source language to destination language using deep-translator.

    Parameters:
        text (str): The text to translate.
        src_lang (str): The source language code (e.g., 'fr' for French, 'auto' for auto-detect).
        dest_lang (str): The destination language code (e.g., 'en' for English).

    Returns:
        str: The translated text.
    """
    # try:
    # the api can translate up to 5000 characters at a time
    if len(text) < 5000:
        # print(len(text), "A")
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    else:
        translated_chunks = []
        # Split the text into chunks by empty lines
        paragraphs = text.split('\n\n')
        paragraphs.append("")
        text_to_translate = ""
        for paragraph in paragraphs:
            if len(text_to_translate) >= 5000:
                # split the chunk into 5000 character subchunks by seperating by spaces and connecting words
                translated_subchunks = []
                text_to_translate_words = text_to_translate.split(" ")
                text_to_translate_words.append("")
                text_to_translate = ""
                for word in text_to_translate_words:
                    if len(text_to_translate) + len(word) >= 4999 or word == text_to_translate_words[-1]:
                        # Translate the accumulated text
                        # print(len(text_to_translate), "B")
                        translated_chunk = GoogleTranslator(source=src_lang, target=dest_lang).translate(text_to_translate)
                        translated_subchunks.append(translated_chunk)
                        text_to_translate = "" + word
                    else:
                        text_to_translate += word + " "

                    # connect the translated subchunks and add this chunk to the translated chunks
                translated_chunk = " ".join(translated_subchunks)
                translated_chunks.append(translated_chunk)
            elif len(text_to_translate) + len(paragraph) >= 5000 or paragraph == paragraphs[-1]:
                # Translate the accumulated text
                # print(len(text_to_translate), "C")
                translated_chunk = GoogleTranslator(source=src_lang, target=dest_lang).translate(text_to_translate)
                translated_chunks.append(translated_chunk)
                text_to_translate = "" + paragraph
            else:
                text_to_translate += paragraph + "\n\n"

        # concatenate the translated chunks
        translated_text = "\n\n".join(translated_chunks)
        return translated_text

    # except Exception as e:
    #     return f"Translation failed: {e}"

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
