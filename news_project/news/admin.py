# admin.py
from django.db.models import Count
from django.contrib import admin
from .models import News, Tag, NewsTag #, UserTag
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'time', 'author']
    search_fields = ['title', 'content']
    list_filter = ['topic','author']

    def changelist_view(self, request, extra_context=None):
        # Get count of news by topic
        news_by_topic = News.objects.values('topic').annotate(total=Count('id'))

        # Get count of news by month
        #news_by_month = News.objects.annotate(month=TruncMonth('time')).values('month').annotate(total=Count('id'))

        # Convert data to dictionaries
        news_by_topic_dict = {item['topic']: item['total'] for item in news_by_topic}
        #news_by_month_dict = {item['month'].strftime('%Y-%m'): item['total'] for item in news_by_month}

        # Create context for the template
        context = {
            'news_by_topic': news_by_topic_dict,
            #'news_by_month': news_by_month_dict,
        }

        return super().changelist_view(request, extra_context=context)

admin.site.register(Tag)
admin.site.register(NewsTag)
#admin.site.register(UserTag)


from django.urls import path
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
import os
import django
from datetime import datetime

class NewsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('crawl-news/', self.process_crawl, name='crawl-news'),
        ]
        return custom_urls + urls

    def process_crawl(self, request):
        # Code from crawl.py
        def your_crawl_function():
            # Thiết lập môi trường Django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
            django.setup()

            url = "https://vnexpress.net/kinh-doanh/chung-khoan"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            article_links = soup.find_all('h2', class_='title-news')
            count = 0

            for link in article_links:
                if count == 15:
                    break

                article_url = link.find('a')['href']
                
                # Truy cập vào trang bài báo
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                # Lấy thông tin từ bài báo
                title = article_soup.find('h1', class_='title-detail').text.strip()
                date = article_soup.find('span', class_='date').text.strip()

                # Lấy tất cả các thẻ <p> và ghép nối nội dung của chúng
                paragraphs = article_soup.find_all('p', class_='Normal')
                content = '\n'.join([p.text.strip() for p in paragraphs])
                
                # Lấy link ảnh
                img_tag = article_soup.find('img', {'class': 'lazy', 'data-src': True})
                link_img = img_tag['data-src'] if img_tag else 'N/A'

                # Topic và author cố định
                topic = 'chứng khoán'
                author = 'VNexpress'
                
                # Lưu thông tin vào cơ sở dữ liệu
                news_item = News(time=date, title=title, content=content, topic=topic, author=author, link_img=link_img)
                news_item.save()

                count += 1

        # Gọi hàm thu thập tin tức
        your_crawl_function()
        
        # Chuyển hướng về trang danh sách tin tức và hiển thị thông báo
        self.message_user(request, "Tin tức đã được thu thập thành công.")
        return HttpResponseRedirect('../')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_crawl_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

#admin.site.register(News, NewsAdmin)


