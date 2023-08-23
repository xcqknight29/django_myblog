import json
from django.http import Http404
from django.shortcuts import render
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

# 使用类视图处理请求
class UserView(APIView):
    # 通过分页器获取用户
    def get(self, request, format=None):
        userList = User.objects.filter(is_active=True)
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=userList, request=request)
        serializer = UserSerializer(result_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    # 添加用户
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'Add success'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    # 根据username修改用户
    def put(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'Update success'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    # 根据username禁用/启用用户
    def delete(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        user.is_active = not user.is_active
        user.save()
        return Response(data={'message': 'Delete success'})

class UserAccoutView(APIView):
    # 用户登录
    def post(self, request, format=None):
        user = get_user_by_username(request.data.get('username'))
        if user.password == request.data.get('password'):
            request.session['username'] = request.data.get('username')
            request.session.set_expiry(0)
            return Response(data={'message': 'Login success'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Login fail, password is wrong'}, status=status.HTTP_401_UNAUTHORIZED)
        
class ArticleView(APIView):
    # 通过分页器获取文章
    def get(self, request, format=None):
        article = Article.objects.all()
        serializer = ArticleSerializer
    # 创建文章
    def post(self, request, format=None):
        return
    # 根据id修改文章
    def put(self, request, format=None):
        return
    # 根据id禁用启用文章
    def delete(self, request, format=None):
        return
        
class ClassificationView(APIView):
    # 获取所有分类
    def get(self, request, format=None):
        return Response(data={'message': 'Get class fail'}, status=status.HTTP_401_UNAUTHORIZED)
    # 创建分类
    def post(self, request, format=None):
        return
    # 修改分类
    def put(self, request, format=None):
        return
    # 禁用、启用分类
    def delete(self, request, format=None):
        return
    
class TagView(APIView):
    # 获取所有Tag
    def get(self, request, format=None):
        return
    # 创建Tag
    def post(self, request, format=None):
        return
    # 修改Tag
    def put(self, request, format=None):
        return
    # 禁用、启用Tag
    def delete(self, request, format=None):
        return
    
# ToDo items:
# 1. User Login
#   * 1. Login check
#   - 2. Request middleware
#   - 3. CORS 
# 2. Article view
#   - 1. Select
#   - 2. Create
#   - 3. Update
#   - 4. Delete
# 3. Classifications view
#   - 1. Select
#   - 2. Create
#   - 3. Update
#   - 4. Delete
# 4. Tag view
#   - 1. Select
#   - 2. Create
#   - 3. Update
#   - 4. Delete