import requests
from bs4 import BeautifulSoup
import csv

url = "https://mobiagri.vn/thong-tin-gia-nong-san/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_links = soup.find_all('h2', class_='post-title')

with open('mobiagri.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    csv_writer.writerow(['Tiêu đề báo', 'Thời gian', 'Nội dung'])

    # Lặp qua từng bài báo và thu thập thông tin
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

        # Ghi thông tin vào file CSV
        csv_writer.writerow([title, date, content])

print("Thông tin đã được lưu vào vnexpress.csv")
