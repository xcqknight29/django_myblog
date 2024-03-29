from django.utils import timezone
from django.db import models

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     name = models.CharField(max_length=40)
#     is_active = models.BooleanField(default=True)
#     competence = models.IntegerField(default=2)
#     last_login = models.DateTimeField(default=timezone.now)
#     join_date = models.DateTimeField(auto_now_add=True)

#     # def __str__(self):
#     #     return f"id: {self.id}, username: {self.username}, password: {self.password}, name: {self.name}, is_active: {self.is_active}, competence: {self.competence}, last_login: {self.last_login}, join_date: {self.join_date}"


# class Classification(models.Model):
#     id = models.AutoField(primary_key=True)
#     classification_name = models.CharField(max_length=20, unique=True)
#     is_active = models.BooleanField(default=True)


# class Tag(models.Model):
#     id = models.AutoField(primary_key=True)
#     tag_name = models.CharField(max_length=20, unique=True)


# class Article(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     classification = models.ForeignKey(Classification, null=True, on_delete=models.SET_NULL)
#     tag = models.ManyToManyField(to=Tag, null=True)
#     create_time = models.DateTimeField(auto_now_add=True)
#     last_update = models.DateTimeField(default=timezone.now)