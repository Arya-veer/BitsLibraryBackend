from django.urls import path
from .views import *

urlpatterns = [
    path("",ExternalLinksListAPI.as_view()),
]