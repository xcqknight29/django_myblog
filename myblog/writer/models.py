from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    competence = models.IntegerField(max_length=1, default=2)
    last_login = models.DateTimeField(auto_now_add=True)
    join_date = models.DateTimeField(auto_now_add=True)

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey()
    