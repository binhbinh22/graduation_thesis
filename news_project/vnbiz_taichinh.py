import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List, Optional

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News, Tag, NewsTag

base_url = 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm'

response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('h3', class_='title')

# Thiết lập Google Generative AI
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

class SearchSchema(BaseModel):
    """Information about an event."""
    chu_the: list[str] = Field(default=None, description="list of product names")
    tinh_chat: list[str] = Field(default=None, description="increase/decrease relationship")
    gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
    nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
format_instructions = pydantic_parser.get_format_instructions()

RECIPE_SEARCH_PROMPT = """
Please return the result in Vietnamese
System
Extraction System
You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
   {format_instructions}
Extract only relevant information from text.
If you don't know the value of a required attribute,
Returns null for the attribute value.
request extract structured information:
  {request}
"""
prompt = ChatPromptTemplate.from_template(
    template=RECIPE_SEARCH_PROMPT,
    partial_variables={
        "format_instructions": format_instructions
    }
)

full_chain = {"request": lambda x: x["request"]} | prompt | llm

def format_extraction_result(result):
    print(f"Raw result content: {result}") 

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        return ""
    
    formatted_result = ""

    for i, chu_the in enumerate(data.get('chu_the', [])):
        tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
        gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
        formatted_result += f"giá {chu_the} {tinh_chat} {gia}\n"
    
    if data.get('nguyen_nhan'):
        formatted_result += "Nguyên nhân:\n"
        for nguyen_nhan in data.get('nguyen_nhan', []):
            formatted_result += f"- {nguyen_nhan}\n"

    return formatted_result.strip()


tag_aliases = {
    "xăng RON 95-III": "xăng RON 95",
    "xăng RON 95-V": "xăng RON 95",
    "xăng E5RON 92": "xăng E5 RON 92",
    "xăng E5 RON92": "xăng E5 RON 92",
    "vàng bạc": "vàng",
    "vàng nguyên liệu": "vàng",
    "vàng miếng": "vàng",
    "giá dầu WTI":"dầu WTI",
    "giá dầu mazut": "dầu mazut",
    "giá xăng E5 RON92" : "xăng E5 RON 92"
}

def normalize_tag(tag_name):
    return tag_aliases.get(tag_name, tag_name)

for article in articles:
    link = article.find('a')['href']
    full_link = f"https://vietnambiz.vn{link}"
    
    article_response = requests.get(full_link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    title = article_soup.find('h1', class_='vnbcb-title').text.strip()
    
    date = article_soup.find('span', class_='vnbcbat-data')['title']
    
    content = article_soup.find('div', class_='vnbcbc-body').text.strip()

    img_link = 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/16/1353891/HN---Vang-016.jpg?w=800&h=496&crop=auto&scale=both'
    topic = 'Tài chính'
    author = 'VietNamBiz'
    
    # Trích xuất thông tin từ nội dung bài viết
    result = full_chain.invoke({"request": content})
    
    # Kiểm tra phản hồi trước khi giải mã JSON
    if result and result.content:
        formatted_result = format_extraction_result(result.content)
    else:
        formatted_result = "No valid response from AI API"

    # Lưu vào cơ sở dữ liệu
    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_link, info_extrac=formatted_result)
    news_item.save()

    # Lưu các chu_the vào bảng Tag và liên kết với News
    extraction_data = json.loads(result.content) if result and result.content else {}
    chu_the_list = extraction_data.get('chu_the', [])
    tinh_chat_list = extraction_data.get('tinh_chat', [])
    for i, chu_the in enumerate(chu_the_list):
        normalized_chu_the = normalize_tag(chu_the)
        tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
        relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
        NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)

    print(f"Saved news item: {title}")

# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News
# base_url = 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm'

# response = requests.get(base_url)
# soup = BeautifulSoup(response.content, 'html.parser')

# articles = soup.find_all('h3', class_='title')

# data = []

# for article in articles:
#     link = article.find('a')['href']
#     full_link = f"https://vietnambiz.vn{link}"
    
#     article_response = requests.get(full_link)
#     article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
#     title = article_soup.find('h1', class_='vnbcb-title').text.strip()
    
#     date = article_soup.find('span', class_='vnbcbat-data')['title']
    
#     content = article_soup.find('div', class_='vnbcbc-body').text.strip()
    
#     # img_tag = article_soup.find('div', class_='vnbcbc-body').find('img')
#     # img_link = img_tag['src'] if img_tag else ''
#     img_link =  'https://cafefcdn.com/203337114487263232/2024/6/9/eu-1717902290974-1717902291353698769808.jpeg'
#     topic = 'Tài chính'
#     author ='VietNamBiz'
#     news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_link)
#     news_item.save()

