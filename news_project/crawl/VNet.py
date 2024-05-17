import requests
from bs4 import BeautifulSoup
import csv

url = "https://vietnamnet.vn/kinh-doanh/thi-truong"

# Tải trang web
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Lấy danh sách các bài báo
article_links = soup.find_all('h3', class_='verticalPost__main-title vnn-title title-bold')

# Mở file CSV để ghi thông tin
with open('VNet.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Tạo đối tượng CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Viết header cho file CSV
    csv_writer.writerow(['Tiêu đề báo', 'Thời gian', 'Nội dung'])

    # Lặp qua từng bài báo và thu thập thông tin
    for link in article_links:
        # Lấy URL từ thẻ a trong thẻ h3
        article_url = "https://vietnamnet.vn" + link.find('a')['href']
        
        # Truy cập vào trang bài báo
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Lấy thông tin từ bài báo
        title = article_soup.find('h1', class_='content-detail-title').text.strip()
        date = article_soup.find('div', class_='bread-crumb-detail__time').text.strip()
        
        # Lấy nội dung từ tất cả các thẻ <p>
        paragraphs = article_soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in paragraphs])

        # Ghi thông tin vào file CSV
        csv_writer.writerow([title, date, content])

        # In thông tin thu thập được
        print("Tiêu đề báo:", title)
        print("Thời gian:", date)
        print("Nội dung:", content)
        print("\n" + "="*50 + "\n")

print("Thông tin đã được lưu vào vietnamnet.csv")

        