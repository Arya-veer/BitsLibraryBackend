from django.urls import path
from .views import *

urlpatterns = [
    path("research_assistance/",ExternalLinksListAPI.as_view()),
    path("open_etds/",OpenETDsListAPI.as_view()),
]