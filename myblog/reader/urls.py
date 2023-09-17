from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.UserMessageView.as_view()),
    path('articleByAuthor', view=views.ArticleAuthorView.as_view()),
    path('articleByClass', view=views.ArticleClassView.as_view()),
    path('self', view=views.UserSelfView.as_view()),
    path('hotClass', view=views.class_hot_view),
    path('newClass', view=views.class_new_view),
    path('searchClass', view=views.class_search_view),
]
