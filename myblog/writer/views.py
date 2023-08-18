from django.shortcuts import render
from .models import User, Article, Classification, Tag
from rest_framework.views import APIView
from rest_framework.response import Response
import serializers

# 使用类视图处理请求
class ArticleView(APIView):
    def get(self, request, format=None):
        article = Article.objects.all()
