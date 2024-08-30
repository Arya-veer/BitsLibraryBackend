from django.urls import path

from .views import *


urlpatterns = [
    path('campuses/',CampusListAPI.as_view()),
    path('ebooks/',EBookListAPI.as_view()),
    path('ejournals/',EJournalListAPI.as_view()),
    path('publishers/',PublisherListAPI.as_view()),
    path('platforms/',PlatformListAPI.as_view()),
    path('donated_books/',DonatedBookListAPI.as_view()),
    path('publications/',PublicationListAPI.as_view()),
]