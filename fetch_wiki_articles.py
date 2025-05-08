import wikipediaapi

def main():
    wiki_article_name = "Six-Day_War"
    print(f"Fetching article: {wiki_article_name}")

    article_text = fetch_wiki_full_text(wiki_article_name, "en")

    print(article_text)


def fetch_wiki_full_text(article_name, article_language):
    """
    Fetch the full text of a Wikipedia article.
    :param article_name: The name of the Wikipedia article.
    :param article_language: The language of the Wikipedia article.
    :return: The full text of the article.
    """
    wiki = wikipediaapi.Wikipedia(user_agent='Dragons',
                                  language=article_language)

    page = wiki.page(article_name)

    if not page.exists():
        print(f"Article '{article_name}' does not exist (this error comes from the script: fetch_wiki_articles.py).")
        return None

    return page.text


if __name__ == '__main__':
    main()

