from django.urls import path
from .views import *

urlpatterns = [
    path("login/",UserLoginAPI.as_view()),
    path("logout/",UserLogoutAPI.as_view()),
    path("profile/",UserProfileAPI.as_view()),
    path("update_phone_number/",PhoneNumberUpdateAPI.as_view()),
    path("items/",ItemListAPI.as_view()),
    path("claim_item/",ClaimItemAPI.as_view()),
    path("claimed_items/",ClaimedItemsAPI.as_view()),
]