from django.urls import path
from .views import *

urlpatterns = [
    path("home/",HomePageAPI.as_view()),
]