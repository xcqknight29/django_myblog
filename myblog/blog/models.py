from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField()
    password = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    identity = models.IntegerField(default=2) # 身份：0=系统管理员 1=创作者 2=读者
    last_login = models.DateTimeField()
    join_time = models.DateTimeField(auto_now_add=True)
