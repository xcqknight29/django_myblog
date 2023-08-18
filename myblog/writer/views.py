from django.shortcuts import render

class ArticleView(APIView):
    def get(self, request, format=None):
        
