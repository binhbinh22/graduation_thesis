import requests
from bs4 import BeautifulSoup
import csv

url = "https://nhandan.vn/thong-tin-hang-hoa/"

# Tải trang web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Lấy danh sách các bài báo
article_links = soup.find_all('h3', class_='story__heading')

# Mở file CSV để ghi thông tin
with open('nhandan.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Viết header cho file CSV
    # Lặp qua từng bài báo và thu thập thông tin
    for link in article_links:
        # Lấy URL từ thẻ a trong thẻ h2
        article_url = link.find('a')['href']
        
        # Truy cập vào trang bài báo
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Lấy thông tin từ bài báo
        title = article_soup.find('h1', class_='article__title cms-title').text.strip()
        date = article_soup.find('time', class_='time').text.strip()
        
        # Lấy tất cả các thẻ <p> và ghép nối nội dung của chúng
        paragraphs = article_soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in paragraphs])

        # Ghi thông tin vào file CSV
        csv_writer.writerow([title, date, content])

