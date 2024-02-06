import json

from django.db.models import Count
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import User, Article, Classification, Tag
from .serializers import UserSerializer, ArticleSerializer, ArticleExcludeContentSerializer, ClassificationSerializer, \
    TagSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# 自定义分页器
class MyPagination:
    pagination = PageNumberPagination()

    def __init__(self):
        self.pagination.page_size = 20
        self.pagination.page_query_param = 'page'
        self.pagination.page_size_query_param = 'size'
        self.pagination.max_page_size = 100

    def paginate_queryset(self, queryset, request):
        result = self.pagination.paginate_queryset(queryset=queryset, request=request)
        return {'total': self.pagination.page.paginator.count, 'data': result}


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


def get_competence(request):
    user = request.session.get('user')
    return user.competence


# 使用类视图处理请求
class UserView(APIView):
    # 通过分页器获取用户
    def get(self, request):
        # user_list = User.objects.filter(is_active=True)
        user_list = User.objects.all()
        pagination = MyPagination()
        result_set = pagination.paginate_queryset(queryset=user_list, request=request)
        serializer = UserSerializer(instance=result_set['data'], many=True)
        result_set['data'] = serializer.data
        return Response(data=result_set, status=status.HTTP_200_OK)

    # 添加用户
    def post(self, request):
        try:
            user = get_user_by_username(request.data.get('username'))
        except:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 根据username修改用户
    def put(self, request):
        try:
            user = get_user_by_username(request.data.get('username'))
        except:
            return Http404
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 根据username禁用/启用用户
    def delete(self, request):
        user = get_user_by_username(request.data.get('username'))
        user.is_active = not user.is_active
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserAccoutView(APIView):
    # 用户登录
    def post(self, request):
        user = get_user_by_username(request.data.get('username'))
        if user.password == request.data.get('password'):
            user.last_login = timezone.now()
            user.save()
            request.session['user'] = request.data
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ArticleView(APIView):
    # 通过分页器获取文章（不带文章内容）
    def get(self, request):
        if request.query_params.get('inputContent'):
            article_list = Article.objects.filter(title__icontains=request.query_params.get('inputContent'))
        else:
            article_list = Article.objects.all()
        pagination = MyPagination()
        result_set = pagination.paginate_queryset(queryset=article_list, request=request)
        serializer = ArticleExcludeContentSerializer(instance=result_set.get('data'), many=True)
        result_set['data'] = serializer.data
        return Response(data=result_set, status=status.HTTP_200_OK)

    # 创建文章
    def post(self, request):
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
    def put(self, request):
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
    def delete(self, request):
        article = get_article_by_title(request.data.get('title'))
        article.is_active = not article.is_active
        article.save()
        return Response(status=status.HTTP_200_OK)


# 返回带文章内容的一篇文章
class ArticleEditView(APIView):
    def get(self, request):
        try:
            article = Article.objects.get(id=int(request.query_params['articleId']))
        except:
            Http404
        serializer = ArticleSerializer(instance=article)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ClassificationView(APIView):
    # 获取所有分类
    def get(self, request):
        class_list = Classification.objects.all().order_by('-id')
        pagination = MyPagination()
        result_set = pagination.paginate_queryset(queryset=class_list, request=request)
        serializer = ClassificationSerializer(instance=result_set['data'], many=True)
        result_set['data'] = serializer.data
        return Response(data=result_set, status=status.HTTP_200_OK)

    # 创建分类
    def post(self, request):
        print(request.data)
        serializer = ClassificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 修改分类
    def put(self, request):
        try:
            classification = Classification.objects.get(classification_name=request.data.get('forward_name'))
        except:
            return Http404
        serializer = ClassificationSerializer(instance=classification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 禁用、启用分类
    def delete(self, request):
        class_name = request.data.get('className')
        _class = Classification.objects.get(classification_name=class_name)
        _class.is_active = not _class.is_active
        _class.save()
        return Response(status=status.HTTP_200_OK)


class TagView(APIView):
    # 获取所有Tag
    def get(self, request):
        articleList = Article.objects.all()
        pagination = MyPagination()
        result_set = pagination.paginate_queryset(queryset=articleList, request=request)
        serializer = ArticleSerializer(instance=result_set['data'], many=True)
        result_set['data'] = serializer.data
        return Response(data=result_set, status=status.HTTP_200_OK)

    # 创建Tag
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 修改Tag
    def put(self, request):
        article = get_article_by_title(request.data.get('title'))
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 禁用、启用Tag
    def delete(self, request):
        article = get_article_by_title(request.data.get('title'))
        article.is_active = not article.is_active
        article.save()
        return Response(status=status.HTTP_200_OK)


# 返回一个用户的信息
class UserMessageView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(username=request.query_params['username'])
        except:
            Http404
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 返回特定用户创作的文章（不带文章内容）
class ArticleAuthorView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(username=request.query_params['username'])
        except:
            Http404
        article_list = Article.objects.filter(author=user.id)
        serializer = ArticleExcludeContentSerializer(instance=article_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 返回特定分类下的文章（不带文章内容）
class ArticleClassView(APIView):
    def get(self, request):
        try:
            classification = Classification.objects.get(classification_name=request.query_params['className'])
        except:
            Http404
        article_list = Article.objects.filter(classification=classification.id)
        pagination = MyPagination()
        result_set = pagination.paginate_queryset(queryset=article_list, request=request)
        serializer = ArticleExcludeContentSerializer(instance=result_set['data'], many=True)
        result_set['data'] = serializer.data
        return Response(data=result_set, status=status.HTTP_200_OK)


# 获取session中存储的user的信息，即已登录用户自身的信息
class UserSelfView(APIView):
    def get(self, request):
        username = request.session.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            Http404
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 返回最多文章的6个分类
@api_view()
def class_hot_view(request):
    class_hot_list = Article.objects.values('classification').annotate(total=Count('id')).order_by('-total')[:6]
    # print(class_hot_list)
    class_list = list()
    for item in class_hot_list:
        classification = Classification.objects.get(id=item.get('classification'))
        class_list.append(classification)
    # print(class_list)
    serializer = ClassificationSerializer(instance=class_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


# 返回最新添加的6个分类
@api_view()
def class_new_view(request):
    class_list = Classification.objects.all().order_by('-id')[:6]
    serializer = ClassificationSerializer(instance=class_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


# 分页返回分类搜索结果
@api_view()
def class_search_view(request):
    if (request.query_params.get('className')):
        class_list = Classification.objects.filter(classification_name__icontains=request.query_params.get('className'))
    else:
        class_list = Classification.objects.all().order_by('-id')
    pagination = MyPagination()
    result_set = pagination.paginate_queryset(queryset=class_list, request=request)
    serializer = ClassificationSerializer(instance=result_set['data'], many=True)
    result_set['data'] = serializer.data
    return Response(data=result_set, status=status.HTTP_200_OK)
