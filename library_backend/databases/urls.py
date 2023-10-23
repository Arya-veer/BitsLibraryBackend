from django.urls import path

from .views import *


urlpatterns = [
    path('campuses/',CampusListAPI.as_view()),
    path('trial/',TrialDatabaseListAPI.as_view()),
]