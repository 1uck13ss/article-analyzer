from newspaper import Article

def extract_metadata(article: Article):
    return {
        "title": article.title,
        "author": article.authors,
        "publish_date": article.publish_date.isoformat() if article.publish_date else None
    }