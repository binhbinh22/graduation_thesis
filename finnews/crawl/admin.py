
from django.contrib import admin, messages
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.management import call_command
from subprocess import Popen, PIPE
from .models import Crawls, Topic
admin.site.register(Topic)

def crawl_news_action(request, crawl_id):
    item = Crawls.objects.get(id=crawl_id)
    try:
        base_url = item.url
        topic = item.topic
        author = item.author

        if base_url in ['https://vietnambiz.vn/tai-chinh/ngan-hang.htm', 
                        'https://thanhnien.vn/gia-xang-dau.html', 
                        'https://vietnambiz.vn/hang-hoa/vang.htm', 
                        'https://mobiagri.vn/thong-tin-gia-nong-san/']:
            if base_url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
                call_command('vnbiz_fin')
            elif base_url == 'https://thanhnien.vn/gia-xang-dau.html':
                call_command('crawl_thanhnien')
            elif base_url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
                call_command('vnbiz_gold')    
            elif base_url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
                call_command('mobiagri')
            messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
        else:
            process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic, author], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                messages.success(request, f'Thu thập tin tức {item.topic} thành công cho {item.author}!')
            else:
                messages.error(request, f'Thu thập tin tức {item.topic} thất bại cho {item.author}. Lỗi: {stderr.decode("utf-8")}.')
                
        item.is_collected = True
        item.save()
    except Exception as e:
        messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class CrawlAdmin(admin.ModelAdmin):
    # list_display = ('nguon_tin', 'chu_de', 'duong_dan', 'collect_news_button')
    # list_filter = ('author', 'topic')
    list_display = ('nguon_tin', 'duong_dan', 'collect_news_button')
    list_filter = ('author',)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('crawl/<int:crawl_id>/', self.admin_site.admin_view(crawl_news_action), name='crawl-news'),
        ]
        return custom_urls + urls

    def collect_news_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Thu thập tin</a>',
            self.get_collect_url(obj.id)
        )
    collect_news_button.short_description = 'Thu thập tin'
    collect_news_button.allow_tags = True

    def get_collect_url(self, crawl_id):
        return reverse('admin:crawl-news', args=[crawl_id])
    def chu_de(self, obj):
        return obj.topic
    chu_de.short_description = 'Chủ đề'
    
    def nguon_tin(self, obj):
        return obj.author
    nguon_tin.short_description = 'Nguồn tin'
    
    def duong_dan(self, obj):
        return obj.url
    duong_dan.short_description = 'Đường dẫn'
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
admin.site.register(Crawls, CrawlAdmin)

# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions





# from django.contrib import admin
# from django.contrib import messages
# from .models import Crawl
# from subprocess import Popen, PIPE
# from django.contrib.admin.actions import delete_selected as default_delete_selected

# def crawl_news_action(modeladmin, request, queryset):
#     for item in queryset:
#         try:
#             base_url = item.url
#             topic = item.topic
#             author = item.author

#             if base_url in ['https://vietnambiz.vn/tai-chinh/ngan-hang.htm', 
#                             'https://thanhnien.vn/gia-xang-dau.html', 
#                             'https://vietnambiz.vn/hang-hoa/vang.htm', 
#                             'https://mobiagri.vn/thong-tin-gia-nong-san/']:
#                 if base_url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
#                     call_command('vnbiz_fin')
#                 elif base_url == 'https://thanhnien.vn/gia-xang-dau.html':
#                     call_command('crawl_thanhnien')
#                 elif base_url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
#                     call_command('vnbiz_gold')    
#                 elif base_url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
#                     call_command('mobiagri')
#                 messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
#             else:
#                 process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic, author], stdout=PIPE, stderr=PIPE)
#                 stdout, stderr = process.communicate()
#                 if process.returncode == 0:
#                     messages.success(request, f'Thu thập tin tức {item.topic} thành công cho {item.author}!')
#                 else:
#                     messages.error(request, f'Thu thập tin tức {item.topic} thất bại cho {item.author}. Lỗi: {stderr.decode("utf-8")}.')
                
#                 item.is_collected = True
#                 item.save()
#         except Exception as e:
#             messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

# crawl_news_action.short_description = 'Thu thập tin tức'

# @admin.register(Crawl)
# class CrawlAdmin(admin.ModelAdmin):
#     list_display = ('nguon_tin', 'chu_de', 'duong_dan')
#     list_filter = ('author', 'topic')
#     actions = [crawl_news_action]
#     actions_selection_counter = False
#     def changelist_view(self, request, extra_context=None):
#         self.get_actions(request)
#         return super().changelist_view(request, extra_context)
#     def chu_de(self, obj):
#         return obj.topic
#     chu_de.short_description = 'Chủ đề'
    
#     def nguon_tin(self, obj):
#         return obj.author
#     nguon_tin.short_description = 'Nguồn tin'
    
#     def duong_dan(self, obj):
#         return obj.url
#     duong_dan.short_description = 'Đường dẫn'
    
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


# from django.contrib import admin
# from django.core.management import call_command
# from django.contrib import messages
# from .models import Crawl
# from subprocess import Popen, PIPE
# from django.contrib.admin.actions import delete_selected as default_delete_selected

# def crawl_news_action(modeladmin, request, queryset):
#     for item in queryset:
#         try:
#             base_url = item.url
#             topic = item.topic
#             author = item.author

#             if base_url in ['https://vietnambiz.vn/tai-chinh/ngan-hang.htm', 
#                             'https://thanhnien.vn/gia-xang-dau.html', 
#                             'https://vietnambiz.vn/hang-hoa/vang.htm', 
#                             'https://mobiagri.vn/thong-tin-gia-nong-san/']:
#                 if base_url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
#                     call_command('vnbiz_fin')
#                 elif base_url == 'https://thanhnien.vn/gia-xang-dau.html':
#                     call_command('crawl_thanhnien')
#                 elif base_url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
#                     call_command('vnbiz_gold')    
#                 elif base_url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
#                     call_command('mobiagri')
#                 messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
#             else:
#                 process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic, author], stdout=PIPE, stderr=PIPE)
#                 stdout, stderr = process.communicate()
#                 if process.returncode == 0:
#                     messages.success(request, f'Thu thập tin tức {item.topic} thành công cho {item.author}!')
#                 else:
#                     messages.error(request, f'Thu thập tin tức {item.topic} thất bại cho {item.author}. Lỗi: {stderr.decode("utf-8")}.')
                
#                 item.is_collected = True
#                 item.save()
#         except Exception as e:
#             messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

# crawl_news_action.short_description = 'Thu thập tin tức'

# @admin.register(Crawl)
# class CrawlAdmin(admin.ModelAdmin):
#     list_display = ('nguon_tin', 'chu_de', 'duong_dan')
#     list_filter = ('author', 'topic')
#     actions = [crawl_news_action]
#     def chu_de(self, obj):
#         return obj.topic
#     chu_de.short_description = 'Chủ đề'
#     def nguon_tin(self, obj):
#         return obj.author
#     nguon_tin.short_description = 'Nguồn tin'
#     def duong_dan(self, obj):
#         return obj.url
#     duong_dan.short_description = 'Đường dẫn'
#     def custom_delete_selected(self, request, queryset):
#         return default_delete_selected(self, request, queryset)
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

# from django.contrib import admin
# from django.core.management import call_command
# from django.contrib import messages
# from .models import Crawl
# from django.contrib.admin.actions import delete_selected as default_delete_selected

# def crawl_news_action(modeladmin, request, queryset):
#     for item in queryset:
#         try:
#             if item.url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
#                 call_command('vnbiz_fin')
#             elif item.url == 'https://thanhnien.vn/gia-xang-dau.html':
#                 call_command('crawl_thanhnien')
#             elif item.url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
#                 call_command('vnbiz_gold')    
#             elif item.url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
#                 call_command('mobiagri')
#             messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
#         except Exception as e:
#             messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

# crawl_news_action.short_description = 'Thu thập tin tức'

# @admin.register(Crawl)
# class CrawlAdmin(admin.ModelAdmin):
#     list_display = ('author', 'topic', 'url')
#     list_filter = ('author', 'topic')
#     actions = ['custom_delete_selected']
#     actions = [crawl_news_action]
#     def custom_delete_selected(self, request, queryset):
#         # Phương thức này sẽ ghi đè phương thức xóa mặc định
#         return default_delete_selected(self, request, queryset)
#     custom_delete_selected.short_description = "Xóa"

