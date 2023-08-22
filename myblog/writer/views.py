from django.http import Http404
from django.shortcuts import render
from .models import User, Article, Classification, Tag
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import models
import serializers

# 使用类视图处理请求
class UserView(APIView):
    def get_object(self, username):
        try:
            return models.User.objects.get(username=username)
        except:
            raise Http404
    def get(self, request, format=None):
        user = models.User.objects.all()
        serializer = serializers.UserSerializer(user, many=True)
        return Response(data=serializer.data)
    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, format=None):
        username = request.data
        user = self.get_object(username)
        serializer = serializers.UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, username, format=None):
        username = request.data
class ArticleView(APIView):
    def get(self, request, format=None):
        article = Article.objects.all()
        serializer = serializers.ArticleSerializer
