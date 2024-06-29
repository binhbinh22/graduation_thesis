import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News
base_url = 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm'

response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('h3', class_='title')

data = []

for article in articles:
    link = article.find('a')['href']
    full_link = f"https://vietnambiz.vn{link}"
    
    article_response = requests.get(full_link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    title = article_soup.find('h1', class_='vnbcb-title').text.strip()
    
    date = article_soup.find('span', class_='vnbcbat-data')['title']
    
    content = article_soup.find('div', class_='vnbcbc-body').text.strip()
    
    # img_tag = article_soup.find('div', class_='vnbcbc-body').find('img')
    # img_link = img_tag['src'] if img_tag else ''
    img_link =  'https://cafefcdn.com/203337114487263232/2024/6/9/eu-1717902290974-1717902291353698769808.jpeg'
    topic = 'Tài chính'
    author ='VietNamBiz'
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_link)
    news_item.save()

