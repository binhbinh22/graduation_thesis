import os
import django
import requests
from bs4 import BeautifulSoup
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List, Optional
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News, Tag, NewsTag, KeyReason, NewsReason
from crawl.models import Crawl
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
Please answer accurately and consistently.
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

import re
import json

def remove_unnecessary_characters(json_string):
    cleaned_json = json_string.strip().lstrip('`').lstrip('json').lstrip('```')
    pattern = r'`+'
    cleaned_json = re.sub(pattern, '', cleaned_json)
    return cleaned_json

def format_extraction_result(result):
    clean_result = remove_unnecessary_characters(result)

    if clean_result and clean_result.strip().startswith('{'):
        data = json.loads(clean_result)
        formatted_result = ""

        # Trích xuất thông tin và định dạng kết quả
        for i, chu_the in enumerate(data.get('chu_the', [])):
            dia_diem = data.get('dia_diem', [])[i] if i < len(data.get('dia_diem', [])) else ""
            tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
            gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
            formatted_result += f" {chu_the} {tinh_chat} {gia}.\n"

        if data.get('nguyen_nhan'):
            formatted_result += "Nguyên nhân:\n"
            for nguyen_nhan in data.get('nguyen_nhan', []):
                formatted_result += f"- {nguyen_nhan}\n"

        return formatted_result.strip()
    else:
        return "The LLM response is not a valid JSON string."


#Nguyên nhân
class Classification(BaseModel):
    sentiment: str = Field(..., description="nguyên nhân ảnh hưởng đến sự kiện theo hướng tích cực hoặc tiêu cực", enum=["tích cực", "trung tính", "tiêu cực"])

# Initialize language model and output parser
# parser = PydanticOutputParser(pydantic_object=Classification)

# Define the tagging prompt
tagging_prompt = ChatPromptTemplate.from_template(
    template="""
    Hãy đánh giá xem nguyên nhân có ảnh hưởng tích cực hay tiêu cực đối với sự kiện kinh tế trong văn bản cung cấp.
    Chỉ trả lời "tích cực", "trung tính", hoặc "tiêu cực".
    Trích xuất các thuộc tính được đề cập trong chức năng 'Classification'.
    
    Đoạn văn:
    {input}
    """
)
parser = JsonOutputParser()

# create a chain 
tagging_chain  = tagging_prompt | llm | parser

# Construct the tagging and classification pipeline
tagging_chain = tagging_prompt | llm | parser

# Function to normalize tag names
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

# Loop through crawls
crawls = Crawl.objects.filter(author='Thanh niên')

for crawl in crawls:
    response = requests.get(crawl.url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = soup.find_all('h2', class_='box-title-text')

    for link in article_links:
        article_url = link.find('a')['href']
        article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
            
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        title_tag = article_soup.find('h1', class_='detail-title')
        title = title_tag.find('span').text.strip() if title_tag else 'No title'
            
        date_tag = article_soup.find('div', class_='detail-time')
        date = date_tag.find('div').text.strip() if date_tag else 'No date'

        content_div = article_soup.find('div', class_='detail-cmain')
        paragraphs = content_div.find_all('p') if content_div else []
        content = '\n'.join([p.text.strip() for p in paragraphs])

        img_tag = article_soup.find('a', class_='detail-img-lightbox')
        img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
        topic = crawl.topic.name
        author = crawl.author
        
        # Save the news item to the database
        if crawl.is_extract:
            result = full_chain.invoke({"request": content})
            formatted_result = format_extraction_result(result.content)

            news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
        else:
            news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src)

        news_item.save()

        # Extract tags and relations
        if crawl.is_extract:
            extraction_data = json.loads(result.content)
            chu_the_list = extraction_data.get('chu_the', [])
            tinh_chat_list = extraction_data.get('tinh_chat', [])

            for i, chu_the in enumerate(chu_the_list):
                normalized_chu_the = normalize_tag(chu_the)
                tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
                relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
                NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)

        # Classify reasons for the news item
        # if crawl.is_classify_reasons and crawl.is_extract:
            res = tagging_chain.invoke({"input": formatted_result})
            response_dict = res.dict()
            sentiment = response_dict.get('sentiment', '').lower()

            if sentiment in ["tích cực", "trung tính", "tiêu cực"]:
                key_reasons = KeyReason.objects.all()

                for key_reason in key_reasons:
                    keywords = key_reason.name.split('|')

                    for keyword in keywords:
                        if keyword.lower() in content.lower():
                            key_reason_instance, _ = KeyReason.objects.get_or_create(
                                name=key_reason.name,
                                reason=key_reason.reason
                            )
                            news_reason_instance, created = NewsReason.objects.get_or_create(
                                news=news_item,
                                keyreasons=key_reason_instance,
                                sentiment=sentiment
                            )
                            if created:
                                print(f"Đã lưu nguyên nhân: {key_reason_instance.name} với sentiment: {sentiment} cho tin tức: {news_item.title}")
                            else:
                                print(f"Nguyên nhân: {key_reason_instance.name} đã tồn tại với sentiment: {sentiment} cho tin tức: {news_item.title}")

                            break

print("Quá trình thu thập, trích xuất và phân loại nguyên nhân đã hoàn thành!")


#chạy trích xuất oke 151
# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News, Tag, NewsTag
# from crawl.models import Crawl
# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: list[str] = Field(default=None, description="list of product names")
#     tinh_chat: list[str] = Field(default=None, description="increase/decrease relationship")
#     gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
#     nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

# pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# format_instructions = pydantic_parser.get_format_instructions()

# RECIPE_SEARCH_PROMPT = """
# Please return the result in Vietnamese
# System
# Extraction System
# You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
#    {format_instructions}
# Extract only relevant information from text.
# If you don't know the value of a required attribute,
# Returns null for the attribute value.
# request extract structured information:
#   {request}
# """
# prompt = ChatPromptTemplate.from_template(
#     template=RECIPE_SEARCH_PROMPT,
#     partial_variables={
#         "format_instructions": format_instructions
#     }
# )

# full_chain = {"request": lambda x: x["request"]} | prompt | llm

# import re
# import json

# def remove_unnecessary_characters(json_string):
#     cleaned_json = json_string.strip().lstrip('`').lstrip('json').lstrip('```')
#     pattern = r'`+'
#     cleaned_json = re.sub(pattern, '', cleaned_json)
#     return cleaned_json

# def format_extraction_result(result):
#     clean_result = remove_unnecessary_characters(result)

#     if clean_result and clean_result.strip().startswith('{'):
#         data = json.loads(clean_result)
#         formatted_result = ""

#         # Trích xuất thông tin và định dạng kết quả
#         for i, chu_the in enumerate(data.get('chu_the', [])):
#             dia_diem = data.get('dia_diem', [])[i] if i < len(data.get('dia_diem', [])) else ""
#             tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
#             gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
#             formatted_result += f" {chu_the} {tinh_chat} {gia}.\n"

#         if data.get('nguyen_nhan'):
#             formatted_result += "Nguyên nhân:\n"
#             for nguyen_nhan in data.get('nguyen_nhan', []):
#                 formatted_result += f"- {nguyen_nhan}\n"

#         return formatted_result.strip()
#     else:
#         return "The LLM response is not a valid JSON string."


# tag_aliases = {
#     "xăng RON 95-III": "xăng RON 95",
#     "xăng RON 95-V": "xăng RON 95",
#     "xăng E5RON 92": "xăng E5 RON 92",
#     "xăng E5 RON92": "xăng E5 RON 92",
#     "vàng bạc": "vàng",
#     "vàng nguyên liệu": "vàng",
#     "vàng miếng": "vàng",
#     "giá dầu WTI":"dầu WTI",
#     "giá dầu mazut": "dầu mazut",
#     "giá xăng E5 RON92" : "xăng E5 RON 92"
# }

# def normalize_tag(tag_name):
#     return tag_aliases.get(tag_name, tag_name)

# crawls = Crawl.objects.filter(author='Thanh niên')

# for crawl in crawls:
#     response = requests.get(crawl.url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     article_links = soup.find_all('h2', class_='box-title-text')

#     for link in article_links:
#         article_url = link.find('a')['href']
#         article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
            
#         article_response = requests.get(article_url)
#         article_soup = BeautifulSoup(article_response.text, 'html.parser')

#         title_tag = article_soup.find('h1', class_='detail-title')
#         title = title_tag.find('span').text.strip() if title_tag else 'No title'
            
#         date_tag = article_soup.find('div', class_='detail-time')
#         date = date_tag.find('div').text.strip() if date_tag else 'No date'

#         content_div = article_soup.find('div', class_='detail-cmain')
#         paragraphs = content_div.find_all('p') if content_div else []
#         content = '\n'.join([p.text.strip() for p in paragraphs])

#         img_tag = article_soup.find('a', class_='detail-img-lightbox')
#         img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
#         topic = crawl.topic.name
#         author = crawl.author
        
#         if crawl.is_extract:
#             result = full_chain.invoke({"request": content})
#             formatted_result = format_extraction_result(result.content)

#             news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
#         else:
#             news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src)

#         news_item.save()

#         if crawl.is_extract:
#             extraction_data = json.loads(result.content)
#             chu_the_list = extraction_data.get('chu_the', [])
#             tinh_chat_list = extraction_data.get('tinh_chat', [])

#             for i, chu_the in enumerate(chu_the_list):
#                 normalized_chu_the = normalize_tag(chu_the)
#                 tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
#                 relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
#                 NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)

# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News, Tag, NewsTag

# url = "https://thanhnien.vn/gia-xang-dau.html"

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# article_links = soup.find_all('h2', class_='box-title-text')

# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: list[str] = Field(default=None, description="list of product names")
#     tinh_chat: list[str] = Field(default=None, description="increase/decrease relationship")
#     gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
#     nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

# pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# format_instructions = pydantic_parser.get_format_instructions()

# RECIPE_SEARCH_PROMPT = """
# Please return the result in Vietnamese
# System
# Extraction System
# You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
#    {format_instructions}
# Extract only relevant information from text.
# If you don't know the value of a required attribute,
# Returns null for the attribute value.
# request extract structured information:
#   {request}
# """
# prompt = ChatPromptTemplate.from_template(
#     template=RECIPE_SEARCH_PROMPT,
#     partial_variables={
#         "format_instructions": format_instructions
#     }
# )

# full_chain = {"request": lambda x: x["request"]} | prompt | llm

# def format_extraction_result(result):
#     print(f"Raw result content: {result}") 
#     data = json.loads(result)
#     formatted_result = ""

#     for i, chu_the in enumerate(data.get('chu_the', [])):
#         tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
#         gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
#         formatted_result += f"giá {chu_the} {tinh_chat} {gia}.\n"
    
#     if data.get('nguyen_nhan'):
#         formatted_result += "Nguyên nhân:\n"
#         for nguyen_nhan in data.get('nguyen_nhan', []):
#             formatted_result += f"- {nguyen_nhan}\n"

#     return formatted_result.strip()

# tag_aliases = {
#     "xăng RON 95-III": "xăng RON 95",
#     "xăng RON 95-V": "xăng RON 95",
#     "xăng E5RON 92": "xăng RON 92",
#     "xăng E5 RON92": "xăng RON 92",
#     "vàng bạc": "vàng",
#     "vàng nguyên liệu": "vàng",
#     "vàng miếng": "vàng",
# }

# def normalize_tag(tag_name):
#     return tag_aliases.get(tag_name, tag_name)

# for link in article_links:
#     article_url = link.find('a')['href']
#     article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
        
#     article_response = requests.get(article_url)
#     article_soup = BeautifulSoup(article_response.text, 'html.parser')

#     title_tag = article_soup.find('h1', class_='detail-title')
#     title = title_tag.find('span').text.strip() if title_tag else 'No title'
        
#     date_tag = article_soup.find('div', class_='detail-time')
#     date = date_tag.find('div').text.strip() if date_tag else 'No date'

#     content_div = article_soup.find('div', class_='detail-cmain')
#     paragraphs = content_div.find_all('p') if content_div else []
#     content = '\n'.join([p.text.strip() for p in paragraphs])

#     img_tag = article_soup.find('a', class_='detail-img-lightbox')
#     img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
#     topic = 'Xăng dầu'
#     author = 'Thanh niên'
    
#     result = full_chain.invoke({"request": content})
#     formatted_result = format_extraction_result(result.content)

#     news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
#     news_item.save()

#     extraction_data = json.loads(result.content)
#     chu_the_list = extraction_data.get('chu_the', [])
#     tinh_chat_list = extraction_data.get('tinh_chat', [])

#     for i, chu_the in enumerate(chu_the_list):
#         # Chuẩn hóa tên tag
#         normalized_chu_the = normalize_tag(chu_the)
#         tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
#         relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
#         NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)


# Hàm chuẩn hóa tên tag
# def normalize_tag(tag_name):
#     return tag_aliases.get(tag_name, tag_name)

# for link in article_links:
#     article_url = link.find('a')['href']
#     article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
        
#     article_response = requests.get(article_url)
#     article_soup = BeautifulSoup(article_response.text, 'html.parser')

#     title_tag = article_soup.find('h1', class_='detail-title')
#     title = title_tag.find('span').text.strip() if title_tag else 'No title'
        
#     date_tag = article_soup.find('div', class_='detail-time')
#     date = date_tag.find('div').text.strip() if date_tag else 'No date'

#     content_div = article_soup.find('div', class_='detail-cmain')
#     paragraphs = content_div.find_all('p') if content_div else []
#     content = '\n'.join([p.text.strip() for p in paragraphs])

#     img_tag = article_soup.find('a', class_='detail-img-lightbox')
#     img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
#     topic = 'Xăng dầu'
#     author = 'Thanh niên'
    
#     result = full_chain.invoke({"request": content})
#     formatted_result = format_extraction_result(result.content)

#     news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
#     news_item.save()

#     extraction_data = json.loads(result.content)
#     chu_the_list = extraction_data.get('chu_the', [])
#     tinh_chat_list = extraction_data.get('tinh_chat', [])

#     for i, chu_the in enumerate(chu_the_list):
#         tag, created = Tag.objects.get_or_create(name=chu_the)
#         relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
#         NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)




# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News, Tag, NewsTag

# url = "https://thanhnien.vn/gia-xang-dau.html"

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# article_links = soup.find_all('h2', class_='box-title-text')

# # Thiết lập Google Generative AI
# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: list[str] = Field(default=None, description="list of product names")
#     tinh_chat: list[str] = Field(default=None, description="increase/decrease relationship")
#     gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
#     nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

# pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# format_instructions = pydantic_parser.get_format_instructions()

# RECIPE_SEARCH_PROMPT = """
# Please return the result in Vietnamese
# System
# Extraction System
# You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
#    {format_instructions}
# Extract only relevant information from text.
# If you don't know the value of a required attribute,
# Returns null for the attribute value.
# request extract structured information:
#   {request}
# """
# prompt = ChatPromptTemplate.from_template(
#     template=RECIPE_SEARCH_PROMPT,
#     partial_variables={
#         "format_instructions": format_instructions
#     }
# )

# full_chain = {"request": lambda x: x["request"]} | prompt | llm

# def format_extraction_result(result):
#     data = json.loads(result)
#     formatted_result = ""

#     for i, chu_the in enumerate(data.get('chu_the', [])):
#         tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
#         gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
#         formatted_result += f"{chu_the} {tinh_chat} {gia}\n"
    
#     if data.get('nguyen_nhan'):
#         formatted_result += "Nguyên nhân:\n"
#         for nguyen_nhan in data.get('nguyen_nhan', []):
#             formatted_result += f"- {nguyen_nhan}\n"

#     return formatted_result.strip()

# for link in article_links:
#     article_url = link.find('a')['href']
#     article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
        
#     article_response = requests.get(article_url)
#     article_soup = BeautifulSoup(article_response.text, 'html.parser')

#     title_tag = article_soup.find('h1', class_='detail-title')
#     title = title_tag.find('span').text.strip() if title_tag else 'No title'
        
#     date_tag = article_soup.find('div', class_='detail-time')
#     date = date_tag.find('div').text.strip() if date_tag else 'No date'

#     content_div = article_soup.find('div', class_='detail-cmain')
#     paragraphs = content_div.find_all('p') if content_div else []
#     content = '\n'.join([p.text.strip() for p in paragraphs])

#     img_tag = article_soup.find('a', class_='detail-img-lightbox')
#     img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
#     topic = 'Xăng dầu'
#     author = 'Thanh niên'
    
#     result = full_chain.invoke({"request": content})
#     formatted_result = format_extraction_result(result.content)

#     news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
#     news_item.save()

#     extraction_data = json.loads(result.content)
#     chu_the_list = extraction_data.get('chu_the', [])
    
#     for chu_the in chu_the_list:
#         tag, created = Tag.objects.get_or_create(name=chu_the)
#         NewsTag.objects.get_or_create(news=news_item, tag=tag)

#     print(f"Saved news item: {title}")

# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional

# # Thiết lập môi trường Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News, Tag, NewsTag

# url = "https://thanhnien.vn/gia-xang-dau.html"

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# article_links = soup.find_all('h2', class_='box-title-text')

# # Thiết lập Google Generative AI
# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: list[str] = Field(default=None, description="list of product names")
#     tinh_chat: list[str] = Field(default=None, description="increase/decrease relationship")
#     gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
#     nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

# pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# format_instructions = pydantic_parser.get_format_instructions()

# RECIPE_SEARCH_PROMPT = """
# Please return the result in Vietnamese
# System
# Extraction System
# You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
#    {format_instructions}
# Extract only relevant information from text.
# If you don't know the value of a required attribute,
# Returns null for the attribute value.
# request extract structured information:
#   {request}
# """
# prompt = ChatPromptTemplate.from_template(
#     template=RECIPE_SEARCH_PROMPT,
#     partial_variables={
#         "format_instructions": format_instructions
#     }
# )

# full_chain = {"request": lambda x: x["request"]} | prompt | llm

# def format_extraction_result(result):
#     data = json.loads(result)
#     formatted_result = ""

#     for i, chu_the in enumerate(data.get('chu_the', [])):
#         tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
#         gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
#         formatted_result += f"{chu_the} {tinh_chat} {gia} một lít.\n"
    
#     if data.get('nguyen_nhan'):
#         formatted_result += "Nguyên nhân:\n"
#         for nguyen_nhan in data.get('nguyen_nhan', []):
#             formatted_result += f"- {nguyen_nhan}\n"

#     return formatted_result.strip()

# for link in article_links:
#     article_url = link.find('a')['href']
#     article_url = "https://thanhnien.vn" + article_url if not article_url.startswith('http') else article_url
        
#     article_response = requests.get(article_url)
#     article_soup = BeautifulSoup(article_response.text, 'html.parser')

#     title_tag = article_soup.find('h1', class_='detail-title')
#     title = title_tag.find('span').text.strip() if title_tag else 'No title'
        
#     date_tag = article_soup.find('div', class_='detail-time')
#     date = date_tag.find('div').text.strip() if date_tag else 'No date'

#     content_div = article_soup.find('div', class_='detail-cmain')
#     paragraphs = content_div.find_all('p') if content_div else []
#     content = '\n'.join([p.text.strip() for p in paragraphs])

#     img_tag = article_soup.find('a', class_='detail-img-lightbox')
#     img_src = img_tag.find('img')['src'] if img_tag and img_tag.find('img') else 'https://media-cdn-v2.laodong.vn/storage/newsportal/2024/6/8/1350377/Gia-Xang-Dau-Hom-Nay.jpg?w=660'
#     topic = 'Xăng dầu'
#     author = 'Thanh niên'
    
#     # Trích xuất thông tin từ nội dung bài viết
#     result = full_chain.invoke({"request": content})
#     formatted_result = format_extraction_result(result.content)

#     # Lưu vào cơ sở dữ liệu
#     news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=img_src, info_extrac=formatted_result)
#     news_item.save()


