from django.urls import path
from .views import *

urlpatterns = [
    path("home/",HomePageAPI.as_view()),
    path("faqs/",FreqAskedQuestionsListAPI.as_view()),
    path("feedback/",FeedbackListCreateAPI.as_view()),
]