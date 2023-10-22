from django.urls import path
from .views import *

urlpatterns = [
    path("external_links/",ExternalLinksListAPI.as_view()),
]