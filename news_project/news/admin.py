from django.db.models import Count
from django.contrib import admin
from .models import News, Tag, NewsTag, UserTag, History, Save, Search, NewsSearch, Reason, KeyReason, NewsReason
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


    
# class NewsSearchAdmin(admin.ModelAdmin):
#     list_display = ('search', 'news')
#     list_filter = ['search',]
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
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
#             modeladmin.message_user(request, f"Failed to extract info for: {news.title}", level='error')

#     modeladmin.message_user(request, "Trích xuất tin tức thành công.")
def extract_information(modeladmin, request, queryset):
    for news in queryset:
        result = subprocess.run(
            ['python3', '/Users/macbook/Desktop/web/news_project/news/extraction.py', news.content],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            news.info_extrac = result.stdout
            news.save()
        else:
            error_message = result.stderr if result.stderr else "Unknown error"
            modeladmin.message_user(request, f"Failed to extract info for: {news.title}. Error: {error_message}", level='error')

    modeladmin.message_user(request, "Trích xuất tin tức thành công.")

extract_information.short_description = "Trích xuất thông tin"

def classify_reasons(modeladmin, request, queryset):
    # Lấy tất cả các từ khoá nguyên nhân từ bảng KeyReason
    key_reasons = KeyReason.objects.all()
    
    # Vòng lặp qua từng tin tức trong queryset
    for news in queryset:
        content = news.info_extrac
        
        if not content:
            modeladmin.message_user(request, f"Tin tức chưa có thông tin!")
            continue
        
        for key_reason in key_reasons:
            keywords = key_reason.name.split('|')
            
            # Kiểm tra từng từ khóa
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    # Nếu từ khóa trùng khớp, lưu vào NewsReason
                    key_reason_instance, _ = KeyReason.objects.get_or_create(
                        name=key_reason.name,
                        reason=key_reason.reason
                    )
                    news_reason_instance, _ = NewsReason.objects.get_or_create(
                        news=news,
                        keyreasons=key_reason_instance,
                        
                    )
                    break  # Dừng vòng lặp khi đã phân loại được tin tức
        modeladmin.message_user(request, "Phân loại nguyên nhân thành công!")
        
# def classify_reasons(modeladmin, request, queryset):
#     key_reasons = KeyReason.objects.all()
    
#     for news in queryset:
        
#         content = news.content
        
#         # Kiểm tra xem content có chứa từ khoá của bất kỳ KeyReason nào hay không
#         for key_reason in key_reasons:
#             if any(keyword.lower() in content.lower() for keyword in key_reason.name.split('|')):
#                 # Nếu tìm thấy từ khoá trong content, lưu vào NewsReason
#                 key_reason_instance, _ = KeyReason.objects.get_or_create(
#                     name=key_reason.name,
#                     reason=key_reason.reason
#                 )
#                 news_reason_instance, _ = NewsReason.objects.get_or_create(
#                     news=news,
#                     keyreasons=key_reason_instance
#                 )
#                 break  # Dừng vòng lặp sau khi phân loại được tin tức
        
#     modeladmin.message_user(request, "Phân loại nguyên nhân thành công!")
classify_reasons.short_description = "Phân loại nguyên nhân"
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
    actions = [extract_information,classify_reasons]

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

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
