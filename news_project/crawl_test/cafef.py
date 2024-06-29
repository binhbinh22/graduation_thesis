import requests
from bs4 import BeautifulSoup
import csv

# URL của trang cần trích xuất
url = "https://cafef.vn/tai-chinh-ngan-hang.chn"

# Gửi yêu cầu GET đến trang web
response = requests.get(url)
response.encoding = 'utf-8'

# Phân tích HTML của trang
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm các bài viết
articles = soup.find_all('div', class_='tlitem box-category-item')
with open('cafef.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Tạo đối tượng CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Viết header cho file CSV
    csv_writer.writerow(['Tiêu đề báo', 'Thời gian', 'Nội dung','link ảnh'])
# Duyệt qua từng bài viết để lấy thông tin chi tiết
    for article in articles:
        # Lấy link bài viết
        link = article.find('a')['href']
        # Lấy tiêu đề bài viết
        title = article.find('h1')['title']
        
        # Gửi yêu cầu GET đến trang chi tiết của bài viết
        article_response = requests.get("https://cafef.vn" + link)
        article_response.encoding = 'utf-8'
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Lấy ngày đăng bài viết
        date = article_soup.find('span', class_='pdate').text.strip()
        
        # Lấy nội dung bài viết
        content_div = article_soup.find('div', class_='detail-content afcbc-body')
        content = ""
        if content_div:
            paragraphs = content_div.find_all('p')
            content = "\n".join([para.text.strip() for para in paragraphs])
        
        # Lấy link ảnh
        image_div = content_div.find('figure', class_='VCSortableInPreviewMode')
        img_link = ""
        if image_div:
            img_tag = image_div.find('img')
            if img_tag:
                img_link = img_tag['src']
        csv_writer.writerow([title, date, content, img_link])
        print(f"Title: {title}")
        print(f"Date: {date}")
        print(f"Content: {content}")
        print(f"Image link: {img_link}")
        print(f"Article link: https://cafef.vn{link}")
        print("\n" + "-"*100 + "\n")

