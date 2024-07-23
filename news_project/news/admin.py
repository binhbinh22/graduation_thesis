from django.db.models import Count
from django.contrib import admin
from .models import News, Tag, NewsTag, UserTag, History, Save, Reason, KeyReason, NewsReason
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import subprocess
import json
from django.core.management import call_command
from django.contrib import messages
from django.dispatch import receiver
from django.urls import path, reverse
import re
from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

class Classification(BaseModel):
    sentiment: str = Field(..., description="nguyên nhân ảnh hưởng đến sự kiện theo hướng tích cực hoặc tiêu cực", enum=["tích cực", "trung tính", "tiêu cực"])
parser = PydanticOutputParser(pydantic_object=Classification)

# Define the tagging chain and prompt
# tagging_prompt = ChatPromptTemplate.from_template(
#     """
#     Đánh giá xem nguyên nhân có ảnh hưởng tích cực hay tiêu cực đối với sự kiện kinh tế trong văn bản cung cấp.
#     Kết quả chỉ trả lời "positive" hoặc "negative", chỉ đưa ra một 'Classification' duy nhất và đầu tiên.
#     Chỉ trích xuất các thuộc tính được đề cập trong chức năng 'Classification'.
#     Đoạn văn:
#     {input}
#     """
# )
tagging_prompt = PromptTemplate(
    template="Đánh giá xem nguyên nhân có ảnh hưởng tích cực hay tiêu cực đối với sự kiện kinh tế trong văn bản cung cấp.\n{format_instructions}\n{input}\n",
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro", google_api_key="AIzaSyDbSQs2-ah4Y3ivz2-TlkqjtRM4S8hSs0I")
tagging_chain = tagging_prompt | llm | parser

parser = JsonOutputParser()

# create a chain 
tagging_chain  = tagging_prompt | llm | parser


admin.site.unregister(Group)
admin.site.register(Reason)

    
@admin.register(NewsReason)
class NewsReasonAdmin(admin.ModelAdmin):
    list_display = ( 'news','keyreasons','reason', 'sentiment')
    # list_filter = ['',]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class UserTagInline(admin.TabularInline):
    model = UserTag
    extra = 1
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
class UserAdmin(admin.ModelAdmin):
    inlines = (UserTagInline,)
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'news','relation')
    list_filter = ['tag','relation']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
# class NewsSearchInline(admin.TabularInline):
#     model = NewsSearch
#     extra = 1 

class NewsTagInline(admin.TabularInline):
    model = NewsTag
    extra = 2

# class SearchAdmin(admin.ModelAdmin):
#     # inlines = [NewsSearchInline]
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
    
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Tag

@receiver(pre_save, sender=Tag)
def check_duplicate_tag(sender, instance, **kwargs):
    # Kiểm tra xem tag đã tồn tại hay chưa
    existing_tag = Tag.objects.filter(name__iexact=instance.name).exists()
    if existing_tag:
        raise ValidationError('Tag đã tồn tại. Hãy thêm một Tag khác')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [NewsTagInline]

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    fields = ('name', 'description')
    list_display = ('name', 'description')

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  
            super().save_model(request, obj, form, change)
            messages.success(request, f"Thêm Tag '{obj.name}' thành công!")
        except ValidationError as e:
            messages.error(request, f"Không thể thêm Tag: {e.message}")
            return

    def response_add(self, request, obj, post_url_continue=None):
        opts = self.model._meta
        obj_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name), current_app=self.admin_site.name)
        preserved_filters = self.get_preserved_filters(request)
        redirect_url = obj_url + '?' + preserved_filters

        # Loại bỏ thông báo mặc định
        storage = messages.get_messages(request)
        storage.used = True

        # messages.success(request, f"")

        return HttpResponseRedirect(redirect_url)



# @admin.register(UserTag)
class UserTagAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    list_filter = ['user',]
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Save)
# admin.site.register(Search, SearchAdmin)


# def extract_information(modeladmin, request, queryset):
#     for news in queryset:
#         result = subprocess.run(
#             ['python3', '/Users/macbook/Desktop/web/news_project/news/extraction.py', news.content],
#             capture_output=True,
#             text=True
#         )
#         if result.returncode == 0:
#             news.info_extrac = result.stdout
#             news.save()
#         else:
#             error_message = result.stderr if result.stderr else "Unknown error"
#             modeladmin.message_user(request, f"Failed to extract info for: {news.title}. Error: {error_message}", level='error')

#     modeladmin.message_user(request, "Trích xuất tin tức thành công.")


# def extract_information(modeladmin, request, queryset):
#     for news in queryset:
#         result = subprocess.run(
#             ['python3', '/Users/macbook/Desktop/web/news_project/news/extraction.py', news.content],
#             capture_output=True,
#             text=True
#         )
#         if result.returncode == 0:
#             formatted_result = result.stdout.strip()
#             news.info_extrac = formatted_result
#             news.save()

#             try:
#                 cleaned_result = remove_unnecessary_characters(formatted_result)
#                 extraction_data = json.loads(cleaned_result)
                
#                 chu_the_list = extraction_data.get('chu_the', [])
#                 tinh_chat_list = extraction_data.get('tinh_chat', [])

#                 for i, chu_the in enumerate(chu_the_list):
#                     normalized_chu_the = normalize_tag(chu_the)
#                     tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
#                     relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
#                     NewsTag.objects.get_or_create(news=news, tag=tag, defaults={'relation': relation})

#             except json.JSONDecodeError:
#                 modeladmin.message_user(request, f"Failed to parse extracted info for: {news.title}.", level='error')
#         else:
#             error_message = result.stderr if result.stderr else "Unknown error"
#             modeladmin.message_user(request, f"Failed to extract info for: {news.title}. Error: {error_message}", level='error')

#     modeladmin.message_user(request, "Trích xuất tin tức thành công.")
def extract_information(modeladmin, request, queryset):
    for news in queryset:
        result = subprocess.run(
            ['python3', '/Users/macbook/Desktop/web/news_project/news/extraction.py', news.content],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) < 2:
                modeladmin.message_user(request, f"Failed to extract info for: {news.title}.", level='error')
                continue

            json_result = output_lines[0].strip()
            formatted_result = "\n".join(output_lines[1:]).strip()

            news.info_extrac = formatted_result
            news.save()

            try:
                cleaned_result = remove_unnecessary_characters(json_result)
                extraction_data = json.loads(cleaned_result)
                
                if isinstance(extraction_data, dict):
                    chu_the_list = extraction_data.get('chu_the', [])
                    tinh_chat_list = extraction_data.get('tinh_chat', [])

                    for i, chu_the in enumerate(chu_the_list):
                        normalized_chu_the = normalize_tag(chu_the)
                        tag, created = Tag.objects.get_or_create(name=normalized_chu_the)
                        relation = tinh_chat_list[i] if i < len(tinh_chat_list) else None
                        NewsTag.objects.get_or_create(news=news, tag=tag, defaults={'relation': relation})
                else:
                    modeladmin.message_user(request, f"Extracted data for {news.title} is not a dictionary.", level='error')

            except json.JSONDecodeError as e:
                modeladmin.message_user(request, f"Failed to parse extracted info for: {news.title}. JSONDecodeError: {e}", level='error')
            except AttributeError as e:
                modeladmin.message_user(request, f"Extracted data for {news.title} is not valid. AttributeError: {e}", level='error')
        else:
            error_message = result.stderr if result.stderr else "Unknown error"
            modeladmin.message_user(request, f"Failed to extract info for: {news.title}. Error: {error_message}", level='error')

    modeladmin.message_user(request, "Trích xuất tin tức thành công.")

def normalize_tag(tag_name):
    tag_aliases = {
        "xăng RON 95-III": "xăng RON 95",
        "xăng RON 95-V": "xăng RON 95",
        "xăng E5RON 92": "xăng E5 RON 92",
        "xăng E5 RON92": "xăng E5 RON 92",
        "vàng bạc": "vàng",
        "vàng nguyên liệu": "vàng",
        "vàng miếng": "vàng",
        "giá dầu WTI": "dầu WTI",
        "giá dầu mazut": "dầu mazut",
        "giá xăng E5 RON92": "xăng E5 RON 92"
    }
    return tag_aliases.get(tag_name, tag_name)

def remove_unnecessary_characters(json_string):
    cleaned_json = json_string.strip().lstrip('`').lstrip('json').lstrip('```')
    pattern = r'`+'
    cleaned_json = re.sub(pattern, '', cleaned_json)
    return cleaned_json

extract_information.short_description = "Trích xuất thông tin"

# def classify_reasons(modeladmin, request, queryset):
#     key_reasons = KeyReason.objects.all()
    
#     for news in queryset:
#         content = news.info_extrac
        
#         if not content:
#             modeladmin.message_user(request, f"Tin tức chưa có thông tin!")
#             continue
        
#         for key_reason in key_reasons:
#             keywords = key_reason.name.split('|')
            
#             for keyword in keywords:
#                 if keyword.lower() in content.lower():
#                     key_reason_instance, _ = KeyReason.objects.get_or_create(
#                         name=key_reason.name,
#                         reason=key_reason.reason
#                     )
#                     news_reason_instance, _ = NewsReason.objects.get_or_create(
#                         news=news,
#                         keyreasons=key_reason_instance,
#                     )
#                     break  
#         modeladmin.message_user(request, "Phân loại nguyên nhân thành công!")
        
def classify_reasons_action(modeladmin, request, queryset):
    key_reasons = KeyReason.objects.all()

    for news in queryset:
        content = news.info_extrac
        
        if not content:
            modeladmin.message_user(request, f"Tin tức chưa có thông tin!")
            continue
        
        inp = content
        res = tagging_chain.invoke({"input": inp})
        
        response_dict = res
        
        sentiment = response_dict.get('sentiment', '').lower()  
        
        if sentiment not in ["tích cực", "trung tính", "tiêu cực"]:
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
                    news_reason_instance, created = NewsReason.objects.get_or_create(
                        news=news,
                        keyreasons=key_reason_instance,
                        sentiment=sentiment  
                    )
                    if created:
                        modeladmin.message_user(request, f"Đã lưu nguyên nhân: {key_reason_instance.name} với sentiment: {sentiment} cho tin tức: {news.title}")
                    else:
                        modeladmin.message_user(request, f"Nguyên nhân: {key_reason_instance.name} đã tồn tại với sentiment: {sentiment} cho tin tức: {news.title}")
                    
                    break  
        modeladmin.message_user(request, "Phân loại nguyên nhân thành công!")

classify_reasons_action.short_description = "Phân loại nguyên nhân"
class KeyReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'reason')
    list_filter = ['reason',]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
admin.site.register(KeyReason,KeyReasonAdmin)


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsTagInline]
    list_display = ['tieu_de', 'chu_de', 'thoi_gian', 'tac_gia', 'is_featured', 'thong_tin_trich_xuat']
    search_fields = ['title', 'content']
    list_filter = ['topic', 'author', 'is_featured']
    list_per_page = 10
    list_editable = ['is_featured']
    actions = [extract_information,classify_reasons_action]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def tieu_de(self, obj):
        return obj.title
    tieu_de.short_description = 'Tiêu đề'

    def chu_de(self, obj):
        return obj.topic
    chu_de.short_description = 'Chủ đề'

    def thoi_gian(self, obj):
        return obj.time
    thoi_gian.short_description = 'Thời gian'

    def tac_gia(self, obj):
        return obj.author
    tac_gia.short_description = 'Nguồn tin'

    def thong_tin_trich_xuat(self, obj):
        return obj.info_extrac
    thong_tin_trich_xuat.short_description = 'Thông tin trích xuất'

admin.site.register(News, NewsAdmin)
