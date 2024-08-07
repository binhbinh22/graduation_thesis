#đã cmt 1 lần trước nó chạy oke 
import os
import sys
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Configuring Django settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
# import django
# django.setup()

# from news.models import Tag, NewsTag, News

llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

class SearchSchema(BaseModel):
    """Information about an event."""
    chu_the: list[str] = Field(default=None, description="product name/category/goods/company/business name/currency/exchange rate")
    tinh_chat: list[str] = Field(default=None, description="verbs in financial economics, increase/decrease relationships, buying and selling")
    gia: list[str] = Field(default=None, description="commodity price/quantity/money unit/inventory/profit/revenue/interest rate/exchange rate; If the price is too small under 1000, skip it")
    nguyen_nhan: list[str] = Field(default=None, description="Causes of price fluctuations of goods/companies/enterprises")

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
        for i, chu_the in enumerate(data.get('chu_the', [])):
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

if __name__ == "__main__":
    request = sys.argv[1]
    result = full_chain.invoke({"request": request})
    clean_result = remove_unnecessary_characters(result.content)
    print(json.dumps(clean_result))
    formatted_result = format_extraction_result(result.content)
    print(formatted_result)


# import re
# import sys
# import json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from typing import List, Optional

# class SearchSchema(BaseModel):
#     """Information about an event."""
#     chu_the: list[str] = Field(default=None, description=" list of product names")
#     tinh_chat: list[str] = Field(default=None, description=" increase/decrease relationship ")
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
#         "format_instructions": format_instructions  # passing in the formatting instructions created earlier in place of "format_instructions" placeholder
#     }
# )

# full_chain = {"request": lambda x: x["request"]} | prompt | llm

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
#         for i, chu_the in enumerate(data.get('chu_the', [])):
#             tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
#             gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
#             formatted_result += f"{chu_the} {tinh_chat} {gia}.\n"

#         if data.get('nguyen_nhan'):
#             formatted_result += "Nguyên nhân:\n"
#             for nguyen_nhan in data.get('nguyen_nhan', []):
#                 formatted_result += f"- {nguyen_nhan}\n"

#         return formatted_result.strip()
#     else:
#         return "The LLM response is not a valid JSON string."



# # def format_extraction_result(result):
# #     clean_result = remove_unnecessary_characters(result)

# #     if clean_result and clean_result.strip().startswith('{'):
# #         data = json.loads(clean_result)
# #         formatted_result = ""
# #         for i, chu_the in enumerate(data.get('chu_the', [])):
# #             tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
# #             gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
# #             formatted_result += f"{chu_the} {tinh_chat} {gia}.\n"

# #         if data.get('nguyen_nhan'):
# #             formatted_result += "Nguyên nhân:\n"
# #             for nguyen_nhan in data.get('nguyen_nhan', []):
# #                 formatted_result += f"- {nguyen_nhan}\n"

# #         return formatted_result.strip()
# #     else:
# #         return "The LLM response is not a valid JSON string."

# if __name__ == "__main__":
#     request = sys.argv[1]
#     result = full_chain.invoke({"request": request})
#     formatted_result = format_extraction_result(result.content)
#         # In JSON hợp lệ trước
#         # Convert to JSON and print
#     try:
#         json_result = result.content
#     except Exception as e:
#         json_result = "{}"  # default to empty JSON if error
#         print(f"Error converting to JSON: {e}")

#     # Print JSON valid result and formatted result separately
#     print(json.dumps(result.content))
    
#     # In định dạng mong muốn
#     print(formatted_result)
#     # print(formatted_result)
# #print(result.content)

# # mã chạy oke chưa có Tag
# # import re
# # import sys
# # import json
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain.prompts import PromptTemplate
# # from langchain.chains import LLMChain
# # from langchain_google_genai import GoogleGenerativeAIEmbeddings
# # from langchain.prompts import ChatPromptTemplate
# # from langchain_core.output_parsers import StrOutputParser

# # llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")

# # from langchain_core.pydantic_v1 import BaseModel, Field
# # from langchain.output_parsers import PydanticOutputParser
# # from typing import List, Optional

# # class SearchSchema(BaseModel):
# #     """Information about an event."""
# #     chu_the: list[str] = Field(default=None, description=" list of product names")
# #     tinh_chat: list[str] = Field(default=None, description=" increase/decrease relationship ")
# #     gia: list[str] = Field(default=None, description="price of goods, amount and unit of money")
# #     nguyen_nhan: list[str] = Field(default=None, description="Causes of changes in commodity prices")

# # pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# # format_instructions = pydantic_parser.get_format_instructions()

# # RECIPE_SEARCH_PROMPT = """
# # Please return the result in Vietnamese
# # System
# # Extraction System
# # You are an expert in algorithmic extraction. Your goal is to understand and analyze the requirement to extract structured information on demand.
# #    {format_instructions}
# # Extract only relevant information from text.
# # If you don't know the value of a required attribute,
# # Returns null for the attribute value.
# # request extract structured information:
# #   {request}
# # """
# # prompt = ChatPromptTemplate.from_template(
# #     template=RECIPE_SEARCH_PROMPT,
# #     partial_variables={
# #         "format_instructions": format_instructions  # passing in the formatting instructions created earlier in place of "format_instructions" placeholder
# #     }
# # )

# # full_chain = {"request": lambda x: x["request"]} | prompt | llm

# # # def format_extraction_result(result):
# # #     # print(f"Raw result content: {result}") 

# # #     data = json.loads(result)
# # #     formatted_result = ""

# # #     for i, chu_the in enumerate(data.get('chu_the', [])):
# # #         tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
# # #         gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
# # #         formatted_result += f"giá {chu_the} {tinh_chat} {gia}.\n"
    
# # #     if data.get('nguyen_nhan'):
# # #         formatted_result += "Nguyên nhân:\n"
# # #         for nguyen_nhan in data.get('nguyen_nhan', []):
# # #             formatted_result += f"- {nguyen_nhan}\n"

# # #     return formatted_result.strip()
# # def remove_unnecessary_characters(json_string):
# #     cleaned_json = json_string.strip().lstrip('`').lstrip('json').lstrip('```')
# #     pattern = r'`+'
# #     cleaned_json = re.sub(pattern, '', cleaned_json)
# #     return cleaned_json

# # def format_extraction_result(result):
# #     clean_result = remove_unnecessary_characters(result)

# #     if clean_result and clean_result.strip().startswith('{'):
# #         data = json.loads(clean_result)
# #         formatted_result = ""
# #         for i, chu_the in enumerate(data.get('chu_the', [])):
# #             tinh_chat = data.get('tinh_chat', [])[i] if i < len(data.get('tinh_chat', [])) else ""
# #             gia = data.get('gia', [])[i] if i < len(data.get('gia', [])) else ""
# #             formatted_result += f"{chu_the} {tinh_chat} {gia}.\n"

# #         if data.get('nguyen_nhan'):
# #             formatted_result += "Nguyên nhân:\n"
# #             for nguyen_nhan in data.get('nguyen_nhan', []):
# #                 formatted_result += f"- {nguyen_nhan}\n"

# #         return formatted_result.strip()
# #     else:
# #         return "The LLM response is not a valid JSON string."

# # if __name__ == "__main__":
# #     request = sys.argv[1]
# #     result = full_chain.invoke({"request": request})
# #     formatted_result = format_extraction_result(result.content)
# #     print(formatted_result)




