
from django.db.models import Count
from django.http import Http404
from rest_framework.decorators import api_view
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
        article_list = Article.objects.filter(author=user.id)
        serializer = ArticleExcludeContentSerializer(instance=article_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
# 返回特定分类下的文章（不带文章内容）
class ArticleClassView(APIView):
    def get(self, request, format=None):
        try:
            classification = Classification.objects.get(classification_name=request.query_params['className'])
        except:
            Http404
        article_list = Article.objects.filter(classification=classification.id)
        pagination = get_pagination()
        result_set = pagination.paginate_queryset(queryset=article_list, request=request)
        serializer = ArticleExcludeContentSerializer(instance=result_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
# 获取session中存储的user的信息，即已登录用户自身的信息
class UserSelfView(APIView):
    def get(self, request, format=None):
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
    print(class_hot_list)
    class_list = list()
    for item in class_hot_list:
        classification = Classification.objects.get(id=item.get('classification'))
        class_list.append(classification)
    print(class_list)
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
    if(request.query_params.get('className')):
        class_list = Classification.objects.filter(classification_name__icontains=request.query_params.get('className'))
    else:
        class_list = Classification.objects.all().order_by('-id')
    pagination = get_pagination()
    result_set = pagination.paginate_queryset(queryset=class_list, request=request)
    serializer = ClassificationSerializer(instance=result_set, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)