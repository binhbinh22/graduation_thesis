from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
import django
import os
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
from langchain.output_parsers import PydanticOutputParser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import KeyReason, NewsReason, News

from langchain_google_genai import ChatGoogleGenerativeAI

tagging_prompt = ChatPromptTemplate.from_template(
    """
    Đánh giá xem nguyên nhân có ảnh hưởng tích cực hay tiêu cực đối với sự kiện kinh tế trong văn bản cung cấp.
    Kết quả chỉ trả lời "positive" hoặc "negative".
    Chỉ trích xuất các thuộc tính được đề cập trong chức năng 'Classification'.
    Đoạn văn:
    {input}
    """
)

class Classification(BaseModel):
    sentiment: str = Field(..., description="nguyên nhân ảnh hưởng đến sự kiện theo hướng tích cực hoặc tiêu cực", enum=["positive", "neutral", "negative"])

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")
parser = PydanticOutputParser(pydantic_object=Classification)


tagging_chain = tagging_prompt | llm | parser

def classify_reasons(modeladmin, request, queryset):
    key_reasons = KeyReason.objects.all()

    for news in queryset:
        content = News.info_extrac
        
        if not content:
            modeladmin.message_user(request, f"Tin tức chưa có thông tin!")
            continue
        
        inp = content
        res = tagging_chain.invoke({"input": inp})
        sentiment = res.dict().get('sentiment', '').lower()  
        
        if sentiment not in ['positive', 'neutral', 'negative']:
            modeladmin.message_user(request, f"Không thể phân loại nguyên nhân cho tin tức: {news.title}")
            continue
        
        for key_reason in key_reasons:
            keywords = key_reason.name.split('|')
            
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    key_reason_instance, _ = KeyReason.objects.get_or_create(
                        name=key_reason.name,
                        reason=key_reason.reason
                    )
                    news_reason_instance, _ = NewsReason.objects.get_or_create(
                        news=news,
                        keyreasons=key_reason_instance,
                        sentiment=sentiment  
                    )
                    break  
        modeladmin.message_user(request, "Phân loại nguyên nhân thành công!")
