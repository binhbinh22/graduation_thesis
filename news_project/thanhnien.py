import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News

url = "https://thanhnien.vn/gia-xang-dau.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_links = soup.find_all('h2', class_='box-title-text')
for link in article_links:
        # Lấy URL từ thẻ a trong thẻ h2
    article_url = link.find('a')['href']
    article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
        
        # Truy cập vào trang bài báo
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Lấy thông tin từ bài báo
    title_tag = article_soup.find('h1', class_='detail-title')
    title = title_tag.find('span').text.strip() if title_tag else 'No title'
        
    date_tag = article_soup.find('div', class_='detail-time')
    date = date_tag.find('div').text.strip() if date_tag else 'No date'
        # Lấy tất cả các thẻ <p> trong <div class="detail-cmain"> và ghép nối nội dung của chúng
    content_div = article_soup.find('div', class_='detail-cmain')
    paragraphs = content_div.find_all('p') if content_div else []
    content = '\n'.join([p.text.strip() for p in paragraphs])

        # Lấy link ảnh từ thẻ img
    img_tag = article_soup.find('a', class_='detail-img-lightbox')
    img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'No image'
    topic = 'Xăng dầu'
    author = 'Thanh niên'
        # Ghi thông tin vào file CSV
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src)
    news_item.save()
print("Thông tin đã được lưu")

