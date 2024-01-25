from django.urls import path
from .views import *

urlpatterns = [
    path("rooms/",RoomListAPI.as_view()),
    path("room/<int:id>/",RoomDetailAPI.as_view()),
    path("bookings/",BookingListAPI.as_view()),
    path("booking/<int:id>/",BookingDetailAPI.as_view()),
    path("vacancy/",RoomVacancyCheckAPI.as_view()),
    path("room_book/",BookRoomAPI.as_view()),
    path("cancel_booking/",BookingCancelAPI.as_view()),
]