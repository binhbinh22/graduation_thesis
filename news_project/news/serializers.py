from .models import News, User, Tag, NewsTag , UserTag, History, Save, Search, NewsSearch, Reason
from rest_framework import serializers
from rest_framework import generics

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'
# class TopicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Topic
#         fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'

class NewsSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSearch
        fields = '__all__'

class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = '__all__'
        
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
        fields = ['id','time', 'title', 'content', 'topic', 'author', 'link_img','info_extrac']

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

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'

