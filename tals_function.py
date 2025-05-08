import time

from tqdm import tqdm

from fetch_wiki_articles import fetch_wiki_full_text_given_name, fetch_wiki_full_text_given_page
from translate_text import translate_text

languages = ["he", "ar", "en"]

def split_utl(url):
    # return the article title and the language
    # Example URL: https://en.wikipedia.org/wiki/Six-Day_War

    # Split the URL by '/' and extract the relevant parts
    parts = url.split('/')
    article_title = parts[-1]
    language = parts[2].split('.')[0]  # Remove the '.org' part

    return article_title, language

def tals_function(url, max_tokens=1500):
    """
    This function takes a Wikipedia URL, extracts the articles and translates them into English.
    If any article exceeds `max_tokens`, it is truncated.
    :param url: the Wikipedia URL
    :param max_tokens: the maximum number of tokens to retain from each article
    :return: the original language, the articles in English, and the URLs of the articles
    """
    article_title, original_language = split_utl(url)
    original_language_page = None

    wiki_articles_in_english = {}
    wiki_urls = {}

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

        # Limit to max_tokens (approximated as words)
        trimmed_text = ' '.join(article_text_in_english.split()[:max_tokens])
        wiki_articles_in_english[lang] = trimmed_text

    return original_language, wiki_articles_in_english, wiki_urls


if __name__ == '__main__':
    original_language, wiki_articles_in_english, wiki_urls = tals_function(
        "https://en.wikipedia.org/wiki/Six-Day_War",
        max_tokens=500  # Adjust this number as needed
    )
    pass
