from django.urls import path
from .views import *

urlpatterns = [
    path("overview/",LibraryOverviewAPI.as_view()),
    path("collection/",LibraryCollectionAPI.as_view()),
    path("rules_regulations/",LibraryRulesAndRegulationAPI.as_view()),
    path("committee/",LibraryCommitteeAPI.as_view()),
    path("team/",LibraryTeamAPI.as_view()),
    path("brochure/",LibraryBrochureAPI.as_view()),
    path("user_guide/",LibraryWebsiteUserGuideAPI.as_view()),
    path("calendar/",LibraryCalendarsAPI.as_view()),
    path("desk/",LibrarianDeskAPI.as_view()),
    path("events/",EventListAPI.as_view()),
    path("news/",NewsAPI.as_view()),
    path("marquee/",BookMarqueeAPI.as_view()),
]