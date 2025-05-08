import time

from tqdm import tqdm

from fetch_wiki_articles import fetch_wiki_full_text_given_name, fetch_wiki_full_text_given_page
from translate_text import translate_text

languages = ["ru", "de", "ja", "he", "ar", "en", "fr", "es"]

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
    """
    This function takes a Wikipedia URL, extracts the articles and translates them into english.
    :param url: the wikipedia URL
    :return: the original language, the articles in english and the urls of the articles
    """
    article_title, original_language = split_utl(url)
    original_language_page = None

    wiki_articles_in_english = {}
    wiki_urls = {}

    # Reorder languages to start with the original language
    modified_languages = [original_language] + [lang for lang in languages if lang != original_language]
    for lang in tqdm(modified_languages):
        if lang == original_language:
            article_text_in_lang, lang_url, page = fetch_wiki_full_text_given_name(article_title, lang)
            original_language_page = page
        else:
            article_text_in_lang, lang_url = fetch_wiki_full_text_given_page(original_language_page.langlinks.get(lang))

        wiki_urls[lang] = lang_url

        if lang == "en":
            article_text_in_english = article_text_in_lang
        else:
            article_text_in_english = translate_text(article_text_in_lang, lang, "en")

        wiki_articles_in_english[lang] = article_text_in_english

    return original_language, wiki_articles_in_english, wiki_urls


if __name__ == '__main__':
    original_language, wiki_articles_in_english, wiki_urls = tals_function("https://en.wikipedia.org/wiki/Six-Day_War")
    pass



