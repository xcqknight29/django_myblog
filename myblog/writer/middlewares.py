# writer/middleware.py

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_urls = ['/writer/login']
    def __call__(self, request):
        # before
        if request.path in self.allow_urls:
            pass
        elif request.session.get('username'):
            pass
        elif request.method == 'OPTIONS':
            pass
        else:
            return HttpResponse(content= 'to_login', status=401)
        response = self.get_response(request)
        # after
        return response
        
class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # before
        response = self.get_response(request)
        # after
        response.headers = {'Access-Control-Allow-Origin': 'http://localhost:5173',
                            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                            'Access-Control-Allow-Headers': 'content-type',
                            'Access-Control-Allow-Credentials': 'true',}
        return response