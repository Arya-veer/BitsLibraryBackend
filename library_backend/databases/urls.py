from django.urls import path

from .views import *


url_patterns = [
    path('campuses/',CampusListAPI.as_view(),name='campus-list'),
    path('list/',DatabaseListAPI.as_view(),name='database-list'),
]