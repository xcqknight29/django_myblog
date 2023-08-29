from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.UserView.as_view()),
    path('login', view=views.UserAccoutView.as_view()),
    path('article', view=views.ArticleView.as_view()),
    path('edit', view=views.ArticleEditView.as_view()),
    path('classification', view=views.ClassificationView.as_view()),
]
