from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.UserView.as_view()),
    path('article', view=views.ArticleView.as_view()),
    path('class', view=views.ClassView.as_view()),
    path('tag', view=views.TagView.as_view()),
    path('login', view=views.user_login_view),
    path('edit', view=views.article_edit_view),
]
