from django.urls import path
from .views import *

urlpatterns = [
    path("courses/",CourseList.as_view()),
    path("years/",YearListAPI.as_view()),
    path("",PaperList.as_view()),
    path("textbooks/",TextBookListAPI.as_view()),
]