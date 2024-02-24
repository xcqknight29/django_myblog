from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.UserView.as_view()),
    path('article', view=views.ArticleView.as_view()),
    path('classification', view=views.ClassificationView.as_view()),
    path('login', view=views.user_acccout_view),
    path('edit', view=views.article_edit_view),
]
