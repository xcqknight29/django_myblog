from django.utils import timezone
from django.db import models
from . import models as this_models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    competence = models.IntegerField(default=2)
    last_login = models.DateTimeField(default=timezone.now())
    join_date = models.DateTimeField(auto_now_add=True)

class Classification(models.Model):
    id = models.AutoField(primary_key=True)
    classification_name = models.CharField(max_length=20)
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=20)

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    classification = models.ForeignKey(Classification, null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to=Tag)
    