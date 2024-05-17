from .models import News, User, Tag, NewsTag# , UserTag
from rest_framework import serializers
from rest_framework import generics

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# class UserTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserTag
#         fields = '__all__'

class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GuestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','time', 'title', 'content', 'topic', 'author', 'link_img']

class GuestNewsSearchSerializer(serializers.Serializer):
    event = serializers.CharField(required=False)
    topic = serializers.CharField(required=False)
    location = serializers.CharField(required=False)

class AdminNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



