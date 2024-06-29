from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import GuestNewsSerializer, GuestNewsSearchSerializer, AdminNewsSerializer, AdminUserSerializer, HistorySerializer, SaveSerializer
from .serializers import NewsSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from .models import News, Tag, NewsTag, UserTag, History, Save, Search, NewsSearch, Reason
from rest_framework import generics, filters
from .serializers import TagSerializer,NewsTagSerializer , UserTagSerializer, SearchSerializer, NewsSearchSerializer, ReasonSerializer
from rest_framework.decorators import api_view
from .serializers import NewsSerializer
from .models import Tag,NewsReason, KeyReason

@csrf_exempt
@api_view(['POST'])
#@permission_classes([IsAuthenticated])

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'id': user.id, 'username': user.username, 'message': 'Đăng ký thành công'}, status=201)
        except:
            return JsonResponse({'message': 'Người dùng đã tồn tại'}, status=400)
    return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)


def get_relations(request):
    relations = NewsTag.objects.values_list('relation', flat=True).distinct()
    return JsonResponse(list(relations), safe=False)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Đăng nhập user sau khi xác thực thành công
                return JsonResponse({'id': user.id, 'username': user.username, 'message': 'Đăng nhập thành công'}, status=200)
            else:
                return JsonResponse({'message': 'Thông tin không hợp lệ'}, status=401)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)

@csrf_exempt
def save_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            news_id = data.get('news_id')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'message': 'Người dùng không tồn tại'}, status=404)

            try:
                news = News.objects.get(id=news_id)
            except News.DoesNotExist:
                return JsonResponse({'message': 'Tin tức không tồn tại'}, status=404)

            Save.objects.create(user=user, news=news)
            return JsonResponse({'message': 'Lịch sử đọc tin được lưu thành công'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)

@csrf_exempt
@api_view(['GET'])
def get_save_news(request, user_id):
    try:
        save = Save.objects.filter(user_id=user_id).select_related('news')
        save_news = []
        for entry in save:
            news_data = NewsSerializer(entry.news).data
            save_news.append({
                'id': entry.id,
                'user': entry.user.id,
                'news': entry.news.id,
                'time': news_data['time'],
                'title': news_data['title'],
                'content': news_data['content'],
                'topic': news_data['topic'],
                'author': news_data['author'],
                'link_img': news_data['link_img'],
            })
        return JsonResponse(save_news, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def save_read_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            news_id = data.get('news_id')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'message': 'Người dùng không tồn tại'}, status=404)

            try:
                news = News.objects.get(id=news_id)
            except News.DoesNotExist:
                return JsonResponse({'message': 'Tin tức không tồn tại'}, status=404)

            History.objects.create(user=user, news=news)
            return JsonResponse({'message': 'Lịch sử đọc tin được lưu thành công'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)

@csrf_exempt
@api_view(['GET'])
def get_read_news(request, user_id):
    try:
        history = History.objects.filter(user_id=user_id).select_related('news')
        read_news = []
        for entry in history:
            news_data = NewsSerializer(entry.news).data
            read_news.append({
                'id': entry.id,
                'user': entry.user.id,
                'news': entry.news.id,
                'time': news_data['time'],
                'title': news_data['title'],
                'content': news_data['content'],
                'topic': news_data['topic'],
                'author': news_data['author'],
                'link_img': news_data['link_img'],
            })
        return JsonResponse(read_news, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
def news_search(request, search_id):
    try:
        news_search = NewsSearch.objects.filter(search_id=search_id)
        if not news_search:
            return Response({'message': 'No news found for this search'}, status=404)
        news_ids = [news.news_id for news in news_search]
        news_results = News.objects.filter(id__in=news_ids)
        serializer = NewsSerializer(news_results, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def recommended_news(request, user_id):
    try:
        user_tags = UserTag.objects.filter(user_id=user_id).values_list('tag', flat=True)
        if not user_tags:
            return Response({'message': 'No tags found for this user.'}, status=404)
        news_ids = NewsTag.objects.filter(tag__in=user_tags).values_list('news', flat=True)
        recommended_news = News.objects.filter(id__in=news_ids)
        if not recommended_news:
            return Response({'message': 'No news found for the selected tags.'}, status=404)
        serializer = NewsSerializer(recommended_news, many=True)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
def create_user_tag(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            tag_id = data.get('tag_id')
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'message': 'Người dùng không tồn tại'}, status=404)

            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                return JsonResponse({'message': 'Tag không tồn tại'}, status=404)

            UserTag.objects.create(user=user, tag=tag)
            return JsonResponse({'message': 'Tag saved successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def get_tags(request):
    if request.method == 'GET':
        tags = Tag.objects.all().values('id', 'name')
        return JsonResponse(list(tags), safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def get_reason(request):
    if request.method == 'GET':
        reason = Reason.objects.all().values('id', 'name')
        return JsonResponse(list(reason), safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@api_view(['GET'])
def news_tag(request, tag_id):
    try:
        # Lấy danh sách tin tức tương ứng với search_id
        news_tag = NewsTag.objects.filter(tag_id=tag_id)
        # Kiểm tra xem có tin tức nào không
        if not news_tag:
            return Response({'message': 'No news found for this tag'}, status=404)
        # Lấy danh sách id tin tức
        news_ids = [news.news_id for news in news_tag]
        # Lấy các tin tức từ id
        news_results = News.objects.filter(id__in=news_ids)
        # Serialize kết quả
        serializer = NewsSerializer(news_results, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
def get_searchs(request):
    if request.method == 'GET':
        searchs = Search.objects.all().values('id', 'name')
        return JsonResponse(list(searchs), safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'password','email')
        return JsonResponse(list(users), safe=False)
    
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)

    if request.method == 'GET':
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        }
        return JsonResponse(user_data)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            if 'password' in data and data['password']:
                user.set_password(data['password'])
            user.save()
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse(user_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_relations_by_tag(request, tag_id):
    if request.method == 'GET':
        try:
            tag = Tag.objects.get(id=tag_id)
            news_tags = NewsTag.objects.filter(tag=tag).values_list('relation', flat=True).distinct()
            return JsonResponse(list(news_tags), safe=False)
        except Tag.DoesNotExist:
            return JsonResponse({'error': 'Tag not found'}, status=404)

@csrf_exempt
def get_sentiments(request, reason_id):
    if request.method == 'GET':
        try:
            reason = Reason.objects.get(id=reason_id)
            key_reasons = KeyReason.objects.filter(reason=reason)
            sentiments = NewsReason.objects.filter(keyreasons__in=key_reasons).values_list('sentiment', flat=True).distinct()
            return JsonResponse(list(sentiments), safe=False)
        except Reason.DoesNotExist:
            return JsonResponse({'error': 'Reason not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_news_by_tag_and_relation(request, tag_id, relation):
    if request.method == 'GET':
        try:
            tag = Tag.objects.get(id=tag_id)
            news_tags = NewsTag.objects.filter(tag=tag, relation=relation).select_related('news')
            news_list = []
            for news_tag in news_tags:
                news_item = news_tag.news
                news_dict = {
                    'id': news_item.id,
                    'time': news_item.time,
                    'title': news_item.title,
                    'content': news_item.content,
                    'topic': news_item.topic,
                    'author': news_item.author,
                    'link_img': news_item.link_img,
                    'info_extrac': news_item.info_extrac,
                }
                news_list.append(news_dict)
            return JsonResponse(news_list, safe=False)
        except Tag.DoesNotExist:
            return JsonResponse({'error': 'Tag not found'}, status=404)
        except NewsTag.DoesNotExist:
            return JsonResponse({'error': 'News not found for this tag and relation'}, status=404)


@csrf_exempt
def get_news_by_reason_and_sentiment(request, reason_id, sentiment):
    if request.method == 'GET':
        try:
            reason = Reason.objects.get(id=reason_id)
            key_reasons = KeyReason.objects.filter(reason=reason)
            news_reasons = NewsReason.objects.filter(keyreasons__in=key_reasons, sentiment=sentiment).select_related('news')
            
            news_list = []
            for news_reason in news_reasons:
                news_item = news_reason.news
                news_dict = {
                    'id': news_item.id,
                    'time': news_item.time,
                    'title': news_item.title,
                    'content': news_item.content,
                    'topic': news_item.topic,
                    'author': news_item.author,
                    'link_img': news_item.link_img,
                    'info_extrac': news_item.info_extrac,
                }
                news_list.append(news_dict)
                
            return JsonResponse(news_list, safe=False)
        except Reason.DoesNotExist:
            return JsonResponse({'error': 'Reason not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News
from .serializers import NewsSerializer

class SearchNewsAPIView(APIView):
    def get(self, request):
        query = request.GET.get('query', '').strip()
        if query:
            news = News.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        else:
            return Response([])








def custom_logout(request):
    logout(request)
    return redirect('http://localhost:3000/')  # URL của giao diện React

class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# class TopicViewSet(viewsets.ModelViewSet):
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer

class UserTagViewSet(viewsets.ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class SaveViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer

class NewsTagViewSet(viewsets.ModelViewSet):
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer


class FeaturedNewsList(generics.ListAPIView):
    queryset = News.objects.filter(is_featured=True).order_by('-id')
    serializer_class = NewsSerializer
    
class GuestNewsList(generics.ListAPIView):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class GoldNewsList(generics.ListAPIView):
    queryset = News.objects.filter(topic='Giá vàng')
    serializer_class = NewsSerializer

class PetroNewsList(generics.ListAPIView):
    queryset = News.objects.filter(topic='Xăng dầu')
    serializer_class = NewsSerializer

class FinanceNewsList(generics.ListAPIView):
    queryset = News.objects.filter(topic='Tài chính')
    serializer_class = NewsSerializer

class NongsanNewsList(generics.ListAPIView):
    queryset = News.objects.filter(topic='Nông sản')
    serializer_class = NewsSerializer

class ThucphamNewsList(generics.ListAPIView):
    queryset = News.objects.filter(topic='Thực phẩm')
    serializer_class = NewsSerializer


class GuestNewsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = News.objects.all()
        serializer = GuestNewsSerializer(queryset, many=True)
        return Response(serializer.data)

    def search(self, request):
        serializer = GuestNewsSearchSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data.get('event')
            topic = serializer.validated_data.get('topic')
            location = serializer.validated_data.get('location')

            queryset = News.objects.all()
            if event:
                queryset = queryset.filter(title__icontains=event)
            if topic:
                queryset = queryset.filter(topic__icontains=topic)
            if location:
                queryset = queryset.filter(content__icontains=location)

            serializer = GuestNewsSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = AdminNewsSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsSearchViewSet(viewsets.ModelViewSet):
    queryset = NewsSearch.objects.all()
    serializer_class = NewsSearchSerializer
class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer


