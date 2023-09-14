from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.UserMessageView.as_view()),
    path('articleByAuthor', view=views.ArticleAuthorView.as_view()),
    path('articleByClass', view=views.ArticleClassView.as_view())
]
