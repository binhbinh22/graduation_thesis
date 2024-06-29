import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News

url = "https://vnexpress.net/chu-de/gia-vang-1403"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_links = soup.find_all('h2', class_='title-news')
count = 0

for link in article_links:
    if count == 15:
        break

    article_url = link.find('a')['href']
    
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    title = article_soup.find('h1', class_='title-detail').text.strip()
    date = article_soup.find('span', class_='date').text.strip()

    paragraphs = article_soup.find_all('p', class_='Normal')
    content = '\n'.join([p.text.strip() for p in paragraphs])
    
    img_tag = article_soup.find('img', {'class': 'lazy', 'data-src': True})
    link_img = img_tag['data-src'] if img_tag else 'N/A'

    topic = 'Giá vàng'
    author = 'VNexpress'
    
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=link_img)
    news_item.save()

print("Thông tin đã được lưu vào cơ sở dữ liệu")
