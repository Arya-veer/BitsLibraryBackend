from django.urls import path
from .views import *

urlpatterns = [
    path("home/",HomePageAPI.as_view()),
    path("faqs/",FreqAskedQuestionsListAPI.as_view()),
    path("feedback/",FeedbackListCreateAPI.as_view()),
    path("text/<str:static_id>/",WebsiteTextRetrieveAPI.as_view()),
    path("upload/",DataExcelUploadAPI.as_view()),
    path("data_excel_types/",DataExcelTypesListAPI.as_view()),
    path("data_excels/",DataExcelListAPI.as_view()),
    path("data_excel/<int:pk>/",DataExcelDetailAPI.as_view()),
]