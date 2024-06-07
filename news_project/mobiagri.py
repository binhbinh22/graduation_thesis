import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News

url = "https://mobiagri.vn/thong-tin-gia-nong-san/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_links = soup.find_all('h2', class_='post-title')    

for link in article_links:
        # Lấy URL từ thẻ a trong thẻ h2
    article_url = link.find('a')['href']
        
        # Truy cập vào trang bài báo
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Lấy thông tin từ bài báo
    title = article_soup.find('h1', class_='post-title').text.strip()
    date = article_soup.find('span', class_='entry-date').text.strip()
        
        # Lấy tất cả các thẻ <p> và ghép nối nội dung của chúng
    paragraphs = article_soup.find_all('p', style='text-align: justify;')
    content = '\n'.join([p.text.strip() for p in paragraphs])

        # Lấy link ảnh từ thẻ img
    img_tag = article_soup.find('img', class_='attachment-agrios-post-standard size-agrios-post-standard wp-post-image')
    link_img = img_tag['src'] if img_tag else 'No image'
    topic = 'Nông sản'
    author = 'Mobiagri'
        # Ghi thông tin vào file CSV
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=link_img)
    news_item.save()
print("Thông tin đã được lưu")


