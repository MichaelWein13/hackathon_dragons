import wikipediaapi

def fetch_wiki_full_text_given_name(article_name: str, article_language:str) -> tuple:
    """
    Fetch the full text of a Wikipedia article.
    :param article_name: The name of the Wikipedia article.
    :param article_language: The language of the Wikipedia article.
    :return: The full text of the article, the URL of the article, and the page object.
    """
    wiki = wikipediaapi.Wikipedia(user_agent='Dragons',
                                  language=article_language)

    page = wiki.page(article_name)

    if not page.exists():
        print(f"Article '{article_name}' does not exist (this error comes from the script: fetch_wiki_articles.py).")
        return None, None, None

    return page.text, page.fullurl, page

def fetch_wiki_full_text_given_page(page) -> tuple:
    """
    Fetch the full text of a Wikipedia article.
    :param article_name: The name of the Wikipedia article.
    :param article_language: The language of the Wikipedia article.
    :return: The full text of the article, the URL of the article, and the page object.
    """

    if not page.exists():
        return None, None, None

    return page.text, page.fullurl


def main():
    wiki_article_name = "Six-Day_War"
    print(f"Fetching article: {wiki_article_name}")
    article_text, url, page = fetch_wiki_full_text_given_name(wiki_article_name, "en")
    print(article_text)

if __name__ == '__main__':
    main()

