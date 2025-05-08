import time

from deep_translator import GoogleTranslator

# {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
def translate_text(text: str, src_lang: str, dest_lang: str = "en") -> str:
    if src_lang == "he":
        src_lang = "iw"
    if dest_lang == "he":
        dest_lang = "iw"

    # text = text.encode('utf-8').decode('utf-8')

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
    length_of_allowed_translation = 2000
    # try:
    # the api can translate up to 5000 characters at a time
    if len(text) < length_of_allowed_translation:
        # print(len(text), "A")
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    else:
        translated_chunks = []
        # Split the text into chunks by empty lines
        paragraphs = text.split('\n\n')
        paragraphs.append("")
        text_to_translate = ""
        for paragraph in paragraphs:
            if len(text_to_translate) >= length_of_allowed_translation:
                # split the chunk into 5000 character subchunks by seperating by spaces and connecting words
                translated_subchunks = []
                text_to_translate_words = text_to_translate.split(" ")
                text_to_translate_words.append("")
                text_to_translate = ""
                for word in text_to_translate_words:
                    if len(text_to_translate) + len(word) >= length_of_allowed_translation or word == text_to_translate_words[-1]:
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
            elif len(text_to_translate) + len(paragraph) >= length_of_allowed_translation or paragraph == paragraphs[-1]:
                # Translate the accumulated text
                # print(len(text_to_translate), "C")
                # print(text_to_translate)
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



def simple_translate(text, src_lang="ru", dest_lang="en"):
    try:
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    except Exception as e:
        print(f"Error: {e}")



if __name__ == '__main__':
    # main()
    ru_text = """Предыстория
Однако в дальнейшем внешнеполитическая обстановка для Насера осложнилась. После серии разногласий Сирия вышла из ОАР. Иракское руководство во главе с Абд аль-Керим Касемом, ранее признававшее Насера общеарабским лидером, начало его критиковать. В Йемене в 1962 году началась гражданская война, куда Насер отправил воевать за одну из сторон около 60 тысяч солдат. Иордания, Саудовская Аравия, Тунис и Марокко также опасались империалистических устремлений Насера. При этом Египет к началу 1960-х находился на грани экономического банкротства. В связи с этим Насер предпочитал выждать более благоприятного времени для войны против Израиля.
В то же время отношения Израиля с Сирией обострились из-за трёх основных факторов: конфликта за водные ресурсы, конфликта за контроль над демилитаризованными зонами вдоль линии прекращения огня 1948 года и поддержки сирийским правительством военизированных группировок палестинских арабов, совершавших диверсии против Израиля. Сирийская артиллерия на Голанских высотах вела систематический обстрел долины Хула. Как писал историк Говард Сакер, сирийцы превратили Голаны «в один огромный военный лагерь, пожертвовав сельскохозяйственным потенциалом этого района».
В 1964 году была создана Организация Освобождения Палестины — террористическая организация палестинских арабов, ставившая целью уничтожение Израиля. Ранее в Кувейте была организована ещё более радикальная группировка палестинских арабов — ФАТХ. Боевиков ООП, называвшихся «Армия освобождения Палестины» Насер разместил на Синае и в Секторе Газа, ФАТХ пользовался поддержкой Сирии и атаковал израильтян из демилитаризованной зоны на севере. Иордания, в отличие от Сирии, пыталась ограничить атаки боевиков со своей территории чтобы не давать Израилю поводов для ответных операций. Тем не менее, в конце-июля — начале августа 1966 года на сессии Совета Безопасности ООН представители Сирии и Иордании не только отказались от какой-либо ответственности за систематические террористические акты, совершавшиеся с их территории, но даже выразили им публичную поддержку. Представитель СССР поддержал эту позицию. Историк Самир Мутави писал, что создание ООП стало главной причиной войны 1967 года. Также в 1964 году было создано Объединённое арабское командование 17 стран Арабской лиги с целью объединения и координации сил арабских государств против Израиля.
13 ноября 1966 года израильские силы в качестве мести за нападения боевиков ФАТХ атаковали деревню Сама на Западном берегу Иордана. В деревне было разрушено 40 зданий, включая мечеть. В бою было убито 18 иорданских солдат. 7 апреля 1967 года очередной пограничный инцидент на сирийско-израильской границе закончился воздушным боем, в котором израильские самолёты сбили 6 сирийских истребителей. Насер отказался вмешиваться и заявил, что договор о взаимной обороне с Сирией применим только в случае полномасштабной войны.
Египет и Сирия пользовались поддержкой Советского Союза. СССР поддерживал стремление Насера запретить проход израильских судов по Суэцкому каналу, а также военные действия сирийцев в демилитаризованной зоне и верховьях реки Иордан. СССР оказывал Египту масштабную финансовую и военную помощь, а также направлял в страну своих военных специалистов. В 1966 году был подписан советско-египетский договор с предоставлением советскому военному флоту в Средиземном море обслуживания в египетских портах, а военно-воздушным силам — три египетских аэродрома. Новое сирийское правительство Салаха Джадида с 1966 года также развернуло тесное военное сотрудничество с СССР. Советская пропаганда демонизировала Израиль, власти высказывали прямые угрозы, а в нападениях ФАТХ начала принимать участие регулярная сирийская армия.
"""
    print(f"Length of text: {len(ru_text)}")
    print(simple_translate(ru_text, "ru", "en"))
