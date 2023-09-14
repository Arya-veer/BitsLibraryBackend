from django.urls import path
from .views import *

urlpatterns = [
    path("overview/",LibraryOverviewAPI.as_view()),
    path("collection/",LibraryCollectionAPI.as_view()),
    path("rules_regulations/",LibraryRulesAndRegulationAPI.as_view()),
    path("committee/",LibraryCommitteeAPI.as_view()),
    path("team/",LibraryTeamAPI.as_view()),
    path("feedback/",FeedbackListAPI.as_view()),
]