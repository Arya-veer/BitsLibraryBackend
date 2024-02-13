from django.urls import path
from .views import *

urlpatterns = [
    path("login/",UserLoginAPI.as_view()),
    path("logout/",UserLogoutAPI.as_view()),
    path("profile/",UserProfileAPI.as_view()),
    path("check_profile/",CheckProfileExists.as_view()),
    path("update_phone_number/",PhoneNumberUpdateAPI.as_view()),
    path("items/",ItemListAPI.as_view()),
    path("add_item/",AddItemAPI.as_view()),
    path("staff_item_list/",StaffItemListAPI.as_view()),
    path("staff_claim_list/",StaffClaimedItemsAPI.as_view()),
    path("claim_item/",ClaimItemAPI.as_view()),
    path("claimed_items/",ClaimedItemsAPI.as_view()),
    path("article_book_request/",ArticleBookRequestListCreateAPI.as_view()),
    path("free_books/",FreeBookListAPI.as_view()),
    path("free_book_request/",FreeBookPickAPI.as_view()),    
]