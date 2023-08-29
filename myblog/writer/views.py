import json
from django.utils import timezone
from django.http import Http404
from .models import User, Article, Classification, Tag
from .serializers import UserSerializer, ArticleSerializer, ClassificationSerializer, TagSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# 自定义分页器
def get_pagination():
    pagination = PageNumberPagination()
    pagination.page_size=20
    pagination.page_query_param = 'page'
    pagination.page_size_query_param = 'size'
    pagination.max_page_size=100
    return pagination

# 通过username查找用户
def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except:
        raise Http404
    
def get_article_by_title(title):
    try:
        return Article.objects.get(title=title)
    except:
        raise Http404

# 使用类视图处理请求
class UserView(APIView):
    # 通过分页器获取用户
    def get(self, request, format=None):
        userList = User.objects.filter(is_active=True)
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=userList, request=request)
        serializer = UserSerializer(instance=result_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    # 添加用户
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 根据username修改用户
    def put(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 根据username禁用/启用用户
    def delete(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        user.is_active = not user.is_active
        user.save()
        return Response(status=status.HTTP_200_OK)

class UserAccoutView(APIView):
    # 用户登录
    def post(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        if user.password == request.data.get('password'):
            user.last_login = timezone.now()
            user.save()
            request.session['username'] = request.data.get('username')
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class ArticleView(APIView):
    # 通过分页器获取文章
    def get(self, request, format=None):
        articleList = Article.objects.all()
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=articleList, request=request)
        serializer = ArticleSerializer(instance=result_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    # 创建文章
    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.session.get('username'))
        except:
            return
        request.data['author'] = user.id
        print(request.data)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 根据id修改文章
    def put(self, request, format=None):
        try:
            article = Article.objects.get(id=request.data.get('id'))
        except: 
            Http404
        article.last_update = timezone.now()
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        # print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 根据id禁用启用文章
    def delete(self, request, format=None):
        article = get_article_by_title(request.data.get('title'))
        article.is_active = not article.is_active
        article.save()
        return Response(status=status.HTTP_200_OK)
    
class ArticleEditView(APIView):
    def get(self, request, format=None):
        try:
            article = Article.objects.get(id=int(request.query_params['articleId']))
        except: 
            Http404
        serializer = ArticleSerializer(instance=article)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
class ClassificationView(APIView):
    # 获取所有分类
    def get(self, request, format=None):
        classList = Classification.objects.all()
        serializer = ClassificationSerializer(instance=classList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    # 创建分类
    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 修改分类
    def put(self, request, format=None):
        article = get_article_by_title(request.data.get('title'))
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 禁用、启用分类
    def delete(self, request, format=None):
        article = get_article_by_title(request.data.get('title'))
        article.is_active = not article.is_active
        article.save()
        return Response(status=status.HTTP_200_OK)
    
class TagView(APIView):
    # 获取所有Tag
    def get(self, request, format=None):
        articleList = Article.objects.all()
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=articleList, request=request)
        serializer = ArticleSerializer(instance=result_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    # 创建Tag
    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 修改Tag
    def put(self, request, format=None):
        article = get_article_by_title(request.data.get('title'))
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # 禁用、启用Tag
    def delete(self, request, format=None):
        article = get_article_by_title(request.data.get('title'))
        article.is_active = not article.is_active
        article.save()
        return Response(status=status.HTTP_200_OK)
    
# ToDo items:
# check 1. User Login
#   check 1. Login check
#   check 2. Request middleware
# check 2. CORS 
# 3. Article
#   - 1. Article view
#       - 1. create article
#       - 2. 
#   - 2. Article page
# 4. User view
# 5. User page