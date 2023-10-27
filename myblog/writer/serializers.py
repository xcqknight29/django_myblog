# writer/serializers.py
from django.utils import timezone
from rest_framework import serializers
from .models import User, Article, Classification, Tag


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    join_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ('id', 'join_date')


class ArticleSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, required=False)
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', default=timezone.now(), required=False)
    author_name = serializers.ReadOnlyField(source='author.name')
    classification_name = serializers.ReadOnlyField(source='classification.classification_name')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id',)


class ArticleExcludeContentSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', default=timezone.now())
    author_name = serializers.ReadOnlyField(source='author.name')
    classification_name = serializers.ReadOnlyField(source='classification.classification_name')

    class Meta:
        model = Article
        exclude = ['content']
        read_only_fields = ('id',)


class ClassificationSerializer(serializers.ModelSerializer):
    article_num = serializers.SerializerMethodField()

    def get_article_num(self, obj):
        return Article.objects.filter(classification=obj.id).count()

    class Meta:
        model = Classification
        fields = '__all__'
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id',)
