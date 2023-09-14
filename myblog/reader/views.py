
from django.http import Http404
from rest_framework.views import APIView
from writer.views import get_pagination
from writer.models import User, Article, Classification, Tag
from writer.serializers import UserSerializer, ArticleSerializer, ArticleExcludeContentSerializer, ClassificationSerializer, TagSerializer
from rest_framework import status
from rest_framework.response import Response

# 返回一个用户的信息
class UserMessageView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(username=request.query_params['username'])
        except:
            Http404
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# 返回特定用户创作的文章（不带文章内容）
class ArticleAuthorView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(username=request.query_params['username'])
        except:
            Http404
        articleList = Article.objects.filter(author=user.id)
        serializer = ArticleExcludeContentSerializer(instance=articleList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
# 返回特定分类下的文章（不带文章内容）
class ArticleClassView(APIView):
    def get(self, request, format=None):
        print(request.query_params['className'])
        try:
            classification = Classification.objects.get(classification_name=request.query_params['className'])
        except:
            Http404
        articleList = Article.objects.filter(classification=classification.id)
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=articleList, request=request)
        serializer = ArticleExcludeContentSerializer(instance=articleList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)