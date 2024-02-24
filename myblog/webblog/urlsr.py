from django.urls import path
from . import views

urlpatterns = [
    path('user', view=views.user_message_view),
    path('articleByAuthor', view=views.article_author_view),
    path('articleByClass', view=views.article_class_view),
    path("self", view=views.user_self_view),
    path('hotClass', view=views.class_hot_view),
    path('newClass', view=views.class_new_view),
    path('searchClass', view=views.class_search_view),
]
