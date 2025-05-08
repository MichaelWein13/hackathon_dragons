from fetch_wiki_articles import fetch_wiki_full_text
from translate_text import translate_text

languages = ["en", "fr", "de", "es", "it", "pt", "ru", "zh", "ja", "ko", "ar", "he"]

def split_utl(url):
    # return the article tile and the language
    # Example URL: https://en.wikipedia.org/wiki/Six-Day_War

    # Split the URL by '/' and extract the relevant parts
    parts = url.split('/')
    # The article title is the last part of the URL
    article_title = parts[-1]
    # The language is the second part of the URL
    language = parts[2].split('.')[0]  # Remove the '.org' part

    return article_title, language

def tals_function(url):
    article_title, original_language = split_utl(url)

    wiki_articles_in_english = {}
    wiki_urls = {}

    for lang in languages:
        if lang in original_language:
            article_name_in_lang = article_title
        else:
            article_name_in_lang = translate_text(article_title, original_language, lang)

        article_text_in_lang, lang_url = fetch_wiki_full_text(article_name_in_lang, lang)
        wiki_urls[lang] = lang_url

        if lang == "en":
            article_text_in_english = article_text_in_lang
        else:
            article_text_in_english = translate_text(article_text_in_lang, lang, "en")

        wiki_articles_in_english[lang] = article_text_in_english

    return original_language, wiki_articles_in_english, wiki_urls


if __name__ == '__main__':
    tals_function("https://en.wikipedia.org/wiki/Six-Day_War")




