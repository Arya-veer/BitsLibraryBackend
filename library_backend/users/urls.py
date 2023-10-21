from django.urls import path
from .views import *

urlpatterns = [
    path("",UserLoginAPI.as_view()),
    path("update_phone_number/",PhoneNumberUpdateAPI.as_view()),
]