# dashboard/views.py

# from django.shortcuts import render
# from news.models import News, Tag
# from django.contrib.admin.views.decorators import staff_member_required
# @staff_member_required
# def admin_dashboard_dashboard(request):
#     num_news = News.objects.count()
#     num_topics = News.objects.values('topic').distinct().count()
#     num_authors = News.objects.values('author').distinct().count()
#     topic_counts = News.objects.values('topic').annotate(count=models.Count('topic')).order_by('-count')
#     tag_counts = Tag.objects.annotate(count=models.Count('newss')).order_by('-count')
#     author_counts = News.objects.values('author').annotate(count=models.Count('author')).order_by('-count')

#     context = {
#         'num_news': num_news,
#         'num_topics': num_topics,
#         'num_authors': num_authors,
#         'topic_counts': {item['topic']: item['count'] for item in topic_counts},
#         'tag_counts': {item.name: item.count for item in tag_counts},
#         'author_counts': {item['author']: item['count'] for item in author_counts},
#     }
#     return render(request, 'dashboard/dashboard.html', context)

# # Dashboard/admin_views.py

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from news.models import News, Tag

@staff_member_required
def admin_dashboard_dashboard(request):
    num_news = News.objects.count()
    num_topics = News.TIME_CHOICES
    topic_counts = {topic[0]: News.objects.filter(topic=topic[0]).count() for topic in num_topics}
    num_tags = Tag.objects.count()
    tag_counts = {tag.name: tag.newss.count() for tag in Tag.objects.all()}
    num_authors = News.objects.count()
    author_counts = {author[0]: News.objects.filter(author=author[0]).count() for author in num_authors}
    context = {
        'num_news': num_news,
        'topic_counts': topic_counts,
        'num_tags': num_tags,
        'tag_counts': tag_counts,
        'author_counts': author_counts,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

