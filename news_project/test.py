from newspaper import Article

def crawl_article(url):
    article = Article(url)
    article.download()
    article.parse()
    
    data = {
        'title': article.title,
        'publish_date': article.publish_date,
        'content': article.text,
        'images': list(article.images)
    }
    
    return data

# Ví dụ sử dụng
url = 'https://thanhnien.vn/gia-xang-dau.html'
article_data = crawl_article(url)
print(article_data)
