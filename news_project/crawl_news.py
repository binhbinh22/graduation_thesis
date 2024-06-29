# import os
# import django
# import requests
# from bs4 import BeautifulSoup
# from newspaper import Article
# from urllib.parse import urljoin
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional
# import sys
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# django.setup()

# from news.models import News, Tag, NewsTag
# from crawl.models import Crawl

# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: List[str] = Field(default=None, description="list of product names")
#     tinh_chat: List[str] = Field(default=None, description="increase/decrease relationship")
#     gia: List[str] = Field(default=None, description="price of goods, amount and unit of money")
#     nguyen_nhan: List[str] = Field(default=None, description="Causes of changes in commodity prices")

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
#         formatted_result += f"giá {chu_the} {tinh_chat} {gia}.\n"
    
#     if data.get('nguyen_nhan'):
#         formatted_result += "Nguyên nhân:\n"
#         for nguyen_nhan in data.get('nguyen_nhan', []):
#             formatted_result += f"- {nguyen_nhan}\n"

#     return formatted_result.strip()

# tag_aliases = {
#     "xăng RON 95-III": "xăng RON 95",
#     "xăng RON 95-V": "xăng RON 95",
#     "xăng E5RON 92": "xăng E5 RON 92",
#     "xăng E5 RON92": "xăng E5 RON 92",
#     "vàng bạc": "vàng",
#     "vàng nguyên liệu": "vàng",
#     "vàng miếng": "vàng",
# }

# def normalize_tag(tag_name):
#     return tag_aliases.get(tag_name, tag_name)

# def scrape_and_extract_article(article_url, topic_name, author, is_extract):
#     try:
#         article = Article(article_url)
#         article.download()
#         article.parse()
        
#         article_soup = BeautifulSoup(article.html, 'html.parser')
        
#         title = article.title
#         content = article.text
        
#         if is_extract:
#             request = f"Extract information from {article_url}"
#             result = full_chain.invoke({"request": content})
#             formatted_result = format_extraction_result(result.content)
            
#             news_item = News.objects.create(
#                 title=title,
#                 content=f"{content}\n\nExtracted information:\n{formatted_result}",
#                 topic=topic_name,
#                 author=author
#             )
#         else:
#             news_item = News.objects.create(
#                 title=title,
#                 content=content,
#                 topic=topic_name,
#                 author=author
#             )
        
#         # Extract tags if needed
#         if is_extract:
#             extraction_data = json.loads(result.content)
#             chu_the_list = extraction_data.get('chu_the', [])
#             tinh_chat_list = extraction_data.get('tinh_chat', [])
            
#             for i, chu_the in enumerate(chu_the_list):
#                 normalized_chu_the = normalize_tag(chu_the)
#                 tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
#                 relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
#                 NewsTag.objects.get_or_create(news=news_item, tag=tag, relation=relation)
        
#         print(f"Article scraped and {'extracted' if is_extract else 'saved'} successfully")
    
#     except Exception as e:
#         print(f"Failed to crawl {article_url}: {e}")

# def scrape_news_site(base_url, topic_name, author):
#     try:
#         crawls = Crawl.objects.filter(url=base_url, author=author)
        
#         for crawl in crawls:
#             response = requests.get(base_url)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             article_links = find_article_links(soup, crawl.site)

#             for link in article_links:
#                 article_url = urljoin(base_url, link.find('a')['href'])
#                 scrape_and_extract_article(article_url, topic_name, author, crawl.is_extract)
        
#         print(f"Thông tin đã được lưu vào cơ sở dữ liệu")
    
#     except Exception as e:
#         print(f"Error scraping site {base_url}: {e}")

# def find_article_links(soup, site):
#     site_mappings = {
#         'vnexpress': {'tag': 'h2', 'class': 'title-news'},
#         'vietnambiz': {'tag': 'h3', 'class': 'title'},
#         'cafef': {'tag': 'h3'},
#         'vneconomy': {'tag': 'h3', 'class': 'story__title'},
#         'tapchicongthuong': {'tag': 'h3','class': 'title title-2 text-left'}
#     }
    
#     if site not in site_mappings:
#         raise ValueError(f"Unsupported site: {site}")
    
#     tag = site_mappings[site].get('tag')
#     class_ = site_mappings[site].get('class')
    
#     if class_:
#         return soup.find_all(tag, class_=class_)
#     else:
#         return soup.find_all(tag)

# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print("Usage: python crawl_news.py <base_url> <topic> <author>")
#         sys.exit(1)
    
#     base_url = sys.argv[1]
#     topic_name = sys.argv[2]  
#     author = sys.argv[3]
    
#     scrape_news_site(base_url, topic_name, author)



import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import News

def get_publish_date(article, article_soup):
    publish_date = article.publish_date.isoformat() if article.publish_date else None
    if publish_date:
        return publish_date
    
    date_tag = article_soup.find('span', class_='date')
    if date_tag:
        return date_tag.text.strip()
    
    return 'N/A'

def scrape_article(article_url, topic_name, author):
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        
        article_soup = BeautifulSoup(article.html, 'html.parser')
        
        title = article.title
        date = get_publish_date(article, article_soup)
        content = article.text
        
        News.objects.create(
            time=date,
            title=title,
            content=content,
            topic=topic_name,  
            author=author,
            link_img=article.top_image if hasattr(article, 'top_image') else None
        )
    except Exception as e:
        print(f"Failed to crawl {article_url}: {e}")

def scrape_news_site(base_url, site, topic_name, author):
    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article_links = find_article_links(soup, site)
        
        for link in article_links:
            article_url = urljoin(base_url, link.find('a')['href'])
            scrape_article(article_url, topic_name, author)
        
        print(f"Thông tin đã được lưu vào cơ sở dữ liệu")
    except Exception as e:
        print(f"Error scraping site {base_url}: {e}")

def find_article_links(soup, site):
    site_mappings = {
        'vnexpress': {'tag': 'h2', 'class': 'title-news'},
        'vietnambiz': {'tag': 'h3', 'class': 'title'},
        'cafef': {'tag': 'h3'},
        'vneconomy': {'tag': 'h3', 'class': 'story__title'},
        'tapchicongthuong': {'tag': 'h3','class': 'title title-2 text-left'}
    }
    
    if site not in site_mappings:
        raise ValueError(f"Unsupported site: {site}")
    
    tag = site_mappings[site].get('tag')
    class_ = site_mappings[site].get('class')
    
    if class_:
        return soup.find_all(tag, class_=class_)
    else:
        return soup.find_all(tag)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python crawl_news.py <base_url> <topic> <author>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    topic_name = sys.argv[2]  
    author = sys.argv[3]
    
    scrape_news_site(base_url, author.lower(), topic_name, author)




