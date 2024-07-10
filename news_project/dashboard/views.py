from django.shortcuts import render
from news.models import News, Tag
from crawl.models import Crawl

def dashboard(request):
    num_url = Crawl.objects.count()-1
    num_news = News.objects.count()
    topics = News.objects.values('topic').distinct()
    num_topics = topics.count()
    topic_counts = {topic['topic']: News.objects.filter(topic=topic['topic']).count() for topic in topics}
    num_tags = Tag.objects.count()
    tag_counts = {tag.name: tag.newss.count() for tag in Tag.objects.all()}
    
    authors = News.objects.values('author').distinct()
    num_authors = authors.count()
    author_counts = {author['author']: News.objects.filter(author=author['author']).count() for author in authors}

    context = {
        'num_url': num_url,
        'num_news': num_news,
        'num_topics': num_topics,
        'topic_counts': topic_counts,
        'num_tags': num_tags,
        'tag_counts': tag_counts,
        'num_authors': num_authors,
        'author_counts': author_counts,
    }

    return render(request, 'dashboard/dashboard.html', context)


# from django.shortcuts import render
# from news.models import News, Tag

# def dashboard(request):
#     num_news = News.objects.count()
#     num_topics = len(News.TIME_CHOICES)
#     topic_counts = {topic[0]: News.objects.filter(topic=topic[0]).count() for topic in News.TIME_CHOICES}
#     num_tags = Tag.objects.count()
#     tag_counts = {tag.name: tag.newss.count() for tag in Tag.objects.all()}
#     num_authors = News.objects.values('author').count()
#     author_counts = {author['author']: News.objects.filter(author=author['author']).count() for author in num_authors}

#     context = {
#         'num_news': num_news,
#         'num_topics': num_topics,
#         'topic_counts': topic_counts,
#         'num_tags': num_tags,
#         'tag_counts': tag_counts,
#         'num_authors': num_authors,
#         'author_counts': author_counts,
#     }

#     return render(request, 'dashboard/dashboard.html', context)


# # # Dashboard/views.py

# # from django.shortcuts import render
# # from news.models import News, Tag

# # def dashboard(request):
# #     num_news = News.objects.count()
# #     num_topics = News.TIME_CHOICES
# #     topic_counts = {topic[0]: News.objects.filter(topic=topic[0]).count() for topic in num_topics}
# #     num_tags = Tag.objects.count()
# #     tag_counts = {tag.name: tag.newss.count() for tag in Tag.objects.all()}
# #     num_authors = News.TIME_CHOICES
# #     author_counts = {author[0]: News.objects.filter(author=author[0]).count() for author in num_authors}
# #     context = {
# #         'num_news': num_news,
# #         'topic_counts': topic_counts,
# #         'num_tags': num_tags,
# #         'tag_counts': tag_counts,
# #         'author_counts': author_counts,

# #     }
    
# #     return render(request, 'dashboard/dashboard.html', context)
