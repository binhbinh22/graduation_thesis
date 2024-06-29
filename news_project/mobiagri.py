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

url = "https://mobiagri.vn/thong-tin-gia-nong-san/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_links = soup.find_all('h2', class_='post-title')

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
    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        return ""
    
    formatted_result = ""

    for i, chu_the in enumerate(data.get('chu_the', [])):
        tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
        gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
        formatted_result += f"giá {chu_the} {tinh_chat} {gia}.\n"
    
    if data.get('nguyen_nhan'):
        formatted_result += "Nguyên nhân:\n"
        for nguyen_nhan in data.get('nguyen_nhan', []):
            formatted_result += f"- {nguyen_nhan}\n"

    return formatted_result.strip()

for link in article_links:
    article_url = link.find('a')['href']
        
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    title = article_soup.find('h1', class_='post-title').text.strip()
    date = article_soup.find('span', class_='entry-date').text.strip()
        
    paragraphs = article_soup.find_all('p', style='text-align: justify;')
    content = '\n'.join([p.text.strip() for p in paragraphs])

    img_tag = article_soup.find('img', class_='attachment-agrios-post-standard size-agrios-post-standard wp-post-image')
    link_img = img_tag['src'] if img_tag else 'No image'
    topic = 'Nông sản'
    author = 'Mobiagri'
    
    try:
        result = full_chain.invoke({"request": content})
        if result and result.content:
            extraction_content = result.content
            formatted_result = format_extraction_result(extraction_content)
        else:
            extraction_content = ""
            formatted_result = "No valid response from AI API"
    except Exception as e:
        extraction_content = ""
        formatted_result = f"Extraction failed: {str(e)}"

    news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=link_img, info_extrac=formatted_result)
    news_item.save()

    try:
        extraction_data = json.loads(extraction_content) if extraction_content else {}
        chu_the_list = extraction_data.get('chu_the', [])
        
        for chu_the in chu_the_list:
            tag, created = Tag.objects.get_or_create(name=chu_the)
            NewsTag.objects.get_or_create(news=news_item, tag=tag)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {str(e)}")

print("Thông tin đã được lưu")
