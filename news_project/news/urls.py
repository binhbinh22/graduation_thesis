from django.urls import path, include
from .views import NewsList, NewsDetail
from rest_framework.routers import DefaultRouter
from .views import GuestNewsViewSet, AdminNewsViewSet, AdminUserViewSet, GuestNewsList
from . import views
from .views import custom_logout
from django.contrib import admin
from .views import TagViewSet, NewsTagViewSet, UserTagViewSet, user_list, HistoryViewSet, SaveViewSet,FeaturedNewsList
# urls.py
from django.urls import path
from .views import SearchNewsAPIView
router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'user-tags', UserTagViewSet)
router.register(r'read_news', HistoryViewSet)
router.register(r'save_news', SaveViewSet)
router.register(r'news-tags', NewsTagViewSet)
router.register(r'guest/news', GuestNewsViewSet, basename='guest_news')
router.register(r'admin/news', AdminNewsViewSet, basename='admin_news')
router.register(r'admin/users', AdminUserViewSet, basename='admin_users')
# router.register(r'searchs', SearchViewSet)
# router.register(r'search_news', NewsSearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('guest/news/', GuestNewsList.as_view(), name='guest_news-list'),
    path('guest/news/featured/', FeaturedNewsList.as_view(), name='featured_news-list'),  
    path('guest/news/<int:pk>/',  NewsDetail.as_view(), name='guest_news-detail'),
    path('guest/news/gold/', views.GoldNewsList.as_view(), name='gold_news-list'),
    path('guest/news/petro/', views.PetroNewsList.as_view(), name='petro_news-list'),
    path('guest/news/finance/', views.FinanceNewsList.as_view(), name='finance_news-list'),
    path('guest/news/nongsan/', views.NongsanNewsList.as_view(), name='nongsan_news-list'),
    path('guest/news/thucpham/', views.ThucphamNewsList.as_view(), name='thucpham_news-list'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('admin/logout/', custom_logout, name='admin_logout'),
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('user-tags/', views.create_user_tag, name='create_user_tag'),
    path('tags/', views.get_tags, name='get_tags'),
    path('reason/', views.get_reason, name='get_reason'),
    path('admin/', admin.site.urls),
    path('recommended-news/<int:user_id>/', views.recommended_news, name='recommended_news'),
    path('read_news/', views.save_read_news, name='save_read_news'),
    path('get_read_news/<int:user_id>/', views.get_read_news, name='get_read_news'),
    path('save_news/', views.save_news, name='save_news'),
    path('get_save_news/<int:user_id>/', views.get_save_news, name='get_save_news'),
    path('search_news/', SearchNewsAPIView.as_view(), name='search_news'),    
    # path('news_search/<int:search_id>/', views.news_search, name='news_search'),
    path('news_tag/<int:tag_id>/', views.news_tag, name='news_tag'),
    path('relations/', views.get_relations,name='relation'),
    path('news_tags/<int:tag_id>/<str:relation>/', views.get_news_by_tag_and_relation, name='get_news_by_tag_and_relation'),
    path('relations/<int:tag_id>/', views.get_relations_by_tag, name='get_relations_by_tag'),
    path('news_reason/<int:reason_id>/<str:sentiment>/', views.get_news_by_reason_and_sentiment, name='get_news_by_reason_and_sentiment'),
    path('sentiments/<int:reason_id>/', views.get_sentiments, name='get_sentiments'),
    # path('api/topics/', get_topics, name='get_topics'),
    path('topics/', views.get_topics, name='get_topics'),
    path('topics/<int:topic_id>/news/', views.get_news_by_topic, name='get_news_by_topic'),

    ]




