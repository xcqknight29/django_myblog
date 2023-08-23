# writer/middleware.py

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_urls = ['/login']
        
    def __call__(self, request):
        # before
        if request.path in self.allow_urls:
            pass
        elif request.session.get('username'):
            pass
        else: 
            return HttpResponseRedirect('/login')
        response = self.get_response(request)
        # after
        return response
        
class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # before
        response = self.get_response(request)
        response.headers = {'Access-Control-Allow-Origin': 'http://localhost:5173', 
                            'Access-Control-Allow-Methods': '*',
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Credentials': 'true',}
        # after
        return response