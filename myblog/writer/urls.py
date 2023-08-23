from django.urls import path
from . import views

urlpatterns = [
    path('user/', view=views.UserView.as_view()),
    path('class/get/', view=views.ClassificationView.as_view()),
]
