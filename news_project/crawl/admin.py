from django.contrib import admin, messages
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.management import call_command
from subprocess import Popen, PIPE
from .models import Crawl, Topic, GroupTag, TopicTag
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

class TopicTagInline(admin.TabularInline):
    model = TopicTag
    extra = 2
# admin.site.register(TopicTag)

class GroupTagAdmin(admin.ModelAdmin):
    inlines = [TopicTagInline]
    list_display = ('name','description')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# admin.site.register(GroupTag,GroupTagAdmin)

@receiver(pre_save, sender=Topic)
def check_duplicate_tag(sender, instance, **kwargs):
    # Kiểm tra xem tag đã tồn tại hay chưa
    existing_topic = Topic.objects.filter(name__iexact=instance.name).exists()
    if existing_topic:
        raise ValidationError('Tag đã tồn tại. Hãy thêm một Tag khác')

#@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicTagInline]
    list_display = ('name','is_show')
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
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

        storage = messages.get_messages(request)
        storage.used = True



        return HttpResponseRedirect(redirect_url)

admin.site.register(Topic,TopicAdmin)


def crawl_news_action(request, crawl_id):
    item = Crawl.objects.get(id=crawl_id)
    try:
        base_url = item.url
        topic_name = item.topic.name  
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
            process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic_name, author], stdout=PIPE, stderr=PIPE)
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
    list_display = ('nguon_tin','chu_de', 'duong_dan','is_extract', 'collect_news_button')
    list_filter = ('author', 'topic')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(topic__is_show=True)

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

admin.site.register(Crawl, CrawlAdmin)

# from django.contrib import admin, messages
# from django.urls import path, reverse
# from django.http import HttpResponseRedirect
# from django.utils.html import format_html
# from django.core.management import call_command
# from subprocess import Popen, PIPE
# from .models import Crawl, Topic

# class TopicAdmin(admin.ModelAdmin):
#     list_display = ('name','is_show')
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
# admin.site.register(Topic,TopicAdmin)

# def crawl_news_action(request, crawl_id):
#     item = Crawl.objects.get(id=crawl_id)
#     try:
#         base_url = item.url
#         topic = item.topic
#         author = item.author

#         if base_url in ['https://vietnambiz.vn/tai-chinh/ngan-hang.htm', 
#                         'https://thanhnien.vn/gia-xang-dau.html', 
#                         'https://vietnambiz.vn/hang-hoa/vang.htm', 
#                         'https://mobiagri.vn/thong-tin-gia-nong-san/']:
#             if base_url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
#                 call_command('vnbiz_fin')
#             elif base_url == 'https://thanhnien.vn/gia-xang-dau.html':
#                 call_command('crawl_thanhnien')
#             elif base_url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
#                 call_command('vnbiz_gold')    
#             elif base_url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
#                 call_command('mobiagri')
#             messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
#         else:
#             process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic, author], stdout=PIPE, stderr=PIPE)
#             stdout, stderr = process.communicate()
#             if process.returncode == 0:
#                 messages.success(request, f'Thu thập tin tức {item.topic} thành công cho {item.author}!')
#             else:
#                 messages.error(request, f'Thu thập tin tức {item.topic} thất bại cho {item.author}. Lỗi: {stderr.decode("utf-8")}.')
                
#         item.is_collected = True
#         item.save()
#     except Exception as e:
#         messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# class CrawlAdmin(admin.ModelAdmin):
#     list_display = ('nguon_tin','chu_de', 'duong_dan', 'collect_news_button')
#     list_filter = ('author', 'topic')

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         return queryset.filter(topic__is_show=True)  # Lọc các mục Crawl dựa trên giá trị của is_show trong Topic

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('crawl/<int:crawl_id>/', self.admin_site.admin_view(crawl_news_action), name='crawl-news'),
#         ]
#         return custom_urls + urls

#     def collect_news_button(self, obj):
#         return format_html(
#             '<a class="button" href="{}">Thu thập tin</a>',
#             self.get_collect_url(obj.id)
#         )
#     collect_news_button.short_description = 'Thu thập tin'
#     collect_news_button.allow_tags = True

#     def get_collect_url(self, crawl_id):
#         return reverse('admin:crawl-news', args=[crawl_id])

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

# admin.site.register(Crawl, CrawlAdmin)

# from django.contrib import admin, messages
# from django.urls import path, reverse
# from django.http import HttpResponseRedirect
# from django.utils.html import format_html
# from django.core.management import call_command
# from subprocess import Popen, PIPE
# from .models import Crawl, Topic
# admin.site.register(Topic)

# def crawl_news_action(request, crawl_id):
#     item = Crawl.objects.get(id=crawl_id)
#     try:
#         base_url = item.url
#         topic = item.topic
#         author = item.author

#         if base_url in ['https://vietnambiz.vn/tai-chinh/ngan-hang.htm', 
#                         'https://thanhnien.vn/gia-xang-dau.html', 
#                         'https://vietnambiz.vn/hang-hoa/vang.htm', 
#                         'https://mobiagri.vn/thong-tin-gia-nong-san/']:
#             if base_url == 'https://vietnambiz.vn/tai-chinh/ngan-hang.htm':
#                 call_command('vnbiz_fin')
#             elif base_url == 'https://thanhnien.vn/gia-xang-dau.html':
#                 call_command('crawl_thanhnien')
#             elif base_url == 'https://vietnambiz.vn/hang-hoa/vang.htm':
#                 call_command('vnbiz_gold')    
#             elif base_url == 'https://mobiagri.vn/thong-tin-gia-nong-san/':
#                 call_command('mobiagri')
#             messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
#         else:
#             process = Popen(['python3', '/Users/macbook/Desktop/web/news_project/crawl_news.py', base_url, topic, author], stdout=PIPE, stderr=PIPE)
#             stdout, stderr = process.communicate()
#             if process.returncode == 0:
#                 messages.success(request, f'Thu thập tin tức {item.topic} thành công cho {item.author}!')
#             else:
#                 messages.error(request, f'Thu thập tin tức {item.topic} thất bại cho {item.author}. Lỗi: {stderr.decode("utf-8")}.')
                
#         item.is_collected = True
#         item.save()
#     except Exception as e:
#         messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# class CrawlAdmin(admin.ModelAdmin):
#     # list_display = ('nguon_tin', 'chu_de', 'duong_dan', 'collect_news_button')
#     # list_filter = ('author', 'topic')
#     list_display = ('nguon_tin', 'duong_dan', 'collect_news_button')
#     #list_filter = ('author',)
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('crawl/<int:crawl_id>/', self.admin_site.admin_view(crawl_news_action), name='crawl-news'),
#         ]
#         return custom_urls + urls

#     def collect_news_button(self, obj):
#         return format_html(
#             '<a class="button" href="{}">Thu thập tin</a>',
#             self.get_collect_url(obj.id)
#         )
#     collect_news_button.short_description = 'Thu thập tin'
#     collect_news_button.allow_tags = True

#     def get_collect_url(self, crawl_id):
#         return reverse('admin:crawl-news', args=[crawl_id])
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
# admin.site.register(Crawl, CrawlAdmin)

# admin.site.register(Topic)
# class TopicAdmin(admin.ModelAdmin):

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
