import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL của trang web
base_url = 'https://vietstock.vn/hang-hoa/vang-va-kim-loai-quy.htm'
root_url = 'https://vietstock.vn'

# Gửi yêu cầu GET đến trang web
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Tìm tất cả các bài báo từ trang chính
articles = soup.find_all('a', class_='fontbold')

# Lưu trữ dữ liệu
data = []
print(articles)
for article in articles:
    # Lấy đường dẫn bài báo
    # link = root_url + article['href']
    link = root_url + link.find('a')['href']
    # Gửi yêu cầu GET đến trang chi tiết của bài báo
    article_response = requests.get(link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    # Lấy tiêu đề
    title = article_soup.find('h1', class_='article-title').text.strip()
    
    # Lấy ngày
    date = article_soup.find('span', class_='date').text.strip()
    
    # Lấy nội dung
    content = article_soup.find('p', class_='pBody').text.strip()
    
    # Lấy link hình ảnh
    img_tag = article_soup.find('td').find('img')
    img_link = img_tag['src'] if img_tag else ''
    
    # Thêm dữ liệu vào danh sách
    data.append([title, date, content, img_link])
for article in articles:
    link = root_url + article['href']
    print(f"Processing article: {link}")
    article_response = requests.get(link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    title_tag = article_soup.find('h1', class_='article-title')
    title = title_tag.text.strip() if title_tag else 'No title found'
    print(f"Title: {title}")
    
    date_tag = article_soup.find('span', class_='date')
    date = date_tag.text.strip() if date_tag else 'No date found'
    print(f"Date: {date}")
    
    content_tag = article_soup.find('p', class_='pBody')
    content = content_tag.text.strip() if content_tag else 'No content found'
    print(f"Content: {content}")
    
    img_tag = article_soup.find('td').find('img')
    img_link = img_tag['src'] if img_tag else 'No image found'
    print(f"Image link: {img_link}")
    
    data.append([title, date, content, img_link])

# Tạo DataFrame từ danh sách dữ liệu
df = pd.DataFrame(data, columns=['Title', 'Date', 'Content', 'Link_img'])

# Lưu DataFrame vào file CSV
df.to_csv('articles.csv', index=False, encoding='utf-8-sig')

print("Dữ liệu đã được lưu vào file articles.csv")
