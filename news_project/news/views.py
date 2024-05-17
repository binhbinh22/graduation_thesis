from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import GuestNewsSerializer, GuestNewsSearchSerializer, AdminNewsSerializer, AdminUserSerializer
from .serializers import NewsSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from .models import News, Tag, NewsTag
from rest_framework import generics, filters
from .serializers import TagSerializer,NewsTagSerializer #, UserTagSerializer
from rest_framework.decorators import api_view
from .serializers import NewsSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# class UserTagViewSet(viewsets.ModelViewSet):
#     queryset = UserTag.objects.all()
#     serializer_class = UserTagSerializer

class NewsTagViewSet(viewsets.ModelViewSet):
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer

class GuestNewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

def search_news(request):
    query = request.GET.get('q', '')
    if query:
        news_list = News.objects.filter(title__icontains=query)
        results = [{'id': news.id, 'title': news.title, 'content': news.content, 'link_img': news.link_img, 'time': news.time, 'topic': news.topic, 'author': news.author} for news in news_list]
    else:
        results = []
    return JsonResponse(results, safe=False)

def custom_logout(request):
    logout(request)
    return redirect('http://localhost:3000/')  # URL của giao diện React

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        try:
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'Tạo thành công'}, status=201)
        except:
            return JsonResponse({'message': 'Lỗi tạo người dùng'}, status=400)
    return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)
# @csrf_exempt
# def register_user(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         try:
#             # Tạo người dùng
#             user = User.objects.create_user(username=username, password=password)
            
#             # Nếu người dùng được tạo thành công, trả về thông báo thành công và ID của người dùng
#             if user:
#                 return JsonResponse({'message': 'Tạo thành công', 'user_id': user.id}, status=201)
#         except Exception as e:
#             # Nếu có lỗi xảy ra, trả về thông báo lỗi
#             return JsonResponse({'message': f'Lỗi tạo người dùng: {str(e)}'}, status=400)
#     return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Thông tin không hợp lệ'}, status=401)
    return JsonResponse({'message': 'Phương thức yêu cầu không hợp lệ'}, status=405)

class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset

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