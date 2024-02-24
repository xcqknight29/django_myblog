from django.utils import timezone
from rest_framework import serializers
from .models import User, Article, Classification, Tag


class UserSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(source='is_active')
    lastLogin = serializers.DateTimeField(source='last_login', format='%Y-%m-%d %H:%M:%S', required=False)
    joinDate = serializers.DateTimeField(source='join_date', format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = User
        exclude = ['password', 'is_active', 'last_login', 'join_date']
        read_only_fields = ('id', 'join_date')


class ArticleSerializer(serializers.ModelSerializer):
    className = serializers.ReadOnlyField(source='classification.classification_name')
    author = serializers.ReadOnlyField(source='author.name')
    createTime = serializers.DateTimeField(source='create_time', format='%Y-%m-%d %H:%M:%S', read_only=True, required=False)
    lastUpdate = serializers.DateTimeField(source='last_update', format='%Y-%m-%d %H:%M:%S', default=timezone.now(), required=False)

    class Meta:
        model = Article
        exclude = ['classification', 'create_time', 'last_update']
        read_only_fields = ('id',)


class ArticleExcludeContentSerializer(serializers.ModelSerializer):
    className = serializers.ReadOnlyField(source='classification.classification_name')
    author = serializers.ReadOnlyField(source='author.name')
    createTime = serializers.DateTimeField(source='create_time', format='%Y-%m-%d %H:%M:%S', read_only=True)
    lastUpdate = serializers.DateTimeField(source='last_update', format='%Y-%m-%d %H:%M:%S', default=timezone.now())
    
    class Meta:
        model = Article
        exclude = ['content', 'classification', 'create_time', 'last_update']
        read_only_fields = ('id',)


class ClassificationSerializer(serializers.ModelSerializer):
    className = serializers.CharField(source='classification_name')
    isActive = serializers.BooleanField(source='is_active')
    articleNum = serializers.SerializerMethodField()

    def get_articleNum(self, obj):
        return Article.objects.filter(classification=obj.id).count()

    class Meta:
        model = Classification
        exclude = ['classification_name', 'is_active']
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    tagName = serializers.CharField(source='tag_name')
    
    class Meta:
        model = Tag
        exclude = ['tag_name']
        read_only_fields = ('id',)
