import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News
# URL của trang web
base_url = 'https://vietnambiz.vn/hang-hoa/vang.htm'

# Gửi yêu cầu GET đến trang web
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Tìm tất cả các bài báo từ trang web
articles = soup.find_all('h3', class_='title')

# Lưu trữ dữ liệu
data = []

for article in articles:
    # Lấy đường dẫn bài báo
    link = article.find('a')['href']
    full_link = f"https://vietnambiz.vn{link}"
    
    # Gửi yêu cầu GET đến trang chi tiết của bài báo
    article_response = requests.get(full_link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    # Lấy tiêu đề
    title = article_soup.find('h1', class_='vnbcb-title').text.strip()
    
    # Lấy ngày
    date = article_soup.find('span', class_='vnbcbat-data')['title']
    
    # Lấy nội dung
    content = article_soup.find('div', class_='vnbcbc-body').text.strip()
    
    # Lấy link hình ảnh (nếu có)
    # img_tag = article_soup.find('div', class_='vnbcbc-body').find('img')
    # img_link = img_tag['src'] if img_tag else ''
    img_link =  ''
    topic = 'Giá vàng'
    author ='VietNamBiz'
    # Thêm dữ liệu vào danh sách
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_link)
    news_item.save()

