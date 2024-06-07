from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import Crawl

def crawl_news_action(modeladmin, request, queryset):
    for item in queryset:
        try:
            if item.topic == 'Tài chính':
                call_command('vnbiz_fin')
            elif item.topic == 'Xăng dầu':
                call_command('crawl_thanhnien')
            elif item.topic == 'Giá vàng':
                call_command('vnbiz_gold')    
            elif item.topic == 'Nông sản':
                call_command('mobiagri')
            messages.success(request, f'Thu thập tin tức {item.topic} thành công!')
        except Exception as e:
            messages.error(request, f'Thu thập tin tức {item.topic} thất bại: {str(e)}')

crawl_news_action.short_description = 'Thu thập tin tức'

@admin.register(Crawl)
class CrawlAdmin(admin.ModelAdmin):
    list_display = ('author', 'topic', 'url')
    actions = [crawl_news_action]

