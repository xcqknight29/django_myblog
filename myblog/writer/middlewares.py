# writer/middleware.py

from django.http import HttpResponse


# 获取当前用户的权限
def get_competence(request):
    user = request.session.get('user')
    return user.competence


# 跳转到登录验证中间件
class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_urls = ['/writer/login']

    def __call__(self, request):
        # before
        if request.path in self.allow_urls:
            pass
        elif request.session.get('user'):
            pass
        elif request.method == 'OPTIONS':
            pass
        else:
            return HttpResponse(content='to_login', status=401)
        response = self.get_response(request)
        # after
        return response


# 权限验证中间件
class CopeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.writer_urls = [
            'writer/article',
            'writer/classification',
            'writer/edit',
        ]
        self.admin_urls = [
            'writer/user',
        ]

    def __call__(self, request):
        # before
        user_comp = get_competence(request)
        if request.method == 'get':
            pass
        if (request.path in self.admin_urls) and (user_comp in [0, 1]):
            return HttpResponse(content='Forbidden', status=403)
        if (request.path in self.writer_urls) and (user_comp == 0):
            return HttpResponse(content='Forbidden', status=403)
        response = self.get_response
        # after
        return response


# 添加cors_header中间件
class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before
        response = self.get_response(request)
        # after
        response.headers = {
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5173',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Allow-Credentials': 'true',
        }
        return response
