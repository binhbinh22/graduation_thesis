
# from django.shortcuts import render
# from django.contrib.admin.views.decorators import staff_member_required
# from news.models import News, Tag
# from crawl.models import Crawl
# @staff_member_required
# def admin_dashboard_dashboard(request):
#     num_url = Crawl.objects.count()
#     num_news = News.objects.count()
#     num_topics = News.TIME_CHOICES
#     topic_counts = {topic[0]: News.objects.filter(topic=topic[0]).count() for topic in num_topics}
#     num_tags = Tag.objects.count()
#     tag_counts = {tag.name: tag.newss.count() for tag in Tag.objects.all()}
#     num_authors = News.objects.count()
#     author_counts = {author[0]: News.objects.filter(author=author[0]).count() for author in num_authors}
#     context = {
#         'num_url': num_url,
#         'num_news': num_news,
#         'topic_counts': topic_counts,
#         'num_tags': num_tags,
#         'tag_counts': tag_counts,
#         'author_counts': author_counts,
#     }
    
#     return render(request, 'dashboard/dashboard.html', context)

