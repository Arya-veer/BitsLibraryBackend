
from rest_framework import views,generics
from rest_framework.permissions import AllowAny

from .serializers import *
# Create your views here.


class LibraryOverviewAPI(generics.RetrieveAPIView):

    serializer_class = LibraryOverviewSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        curr = LibraryOverview.objects.get(is_set = True)
        return curr

class LibraryCollectionAPI(generics.RetrieveAPIView):
    serializer_class = LibraryCollectionSerialzer
    permission_classes = (AllowAny,)

    def get_object(self):
        curr = LibraryCollection.objects.get(is_set = True)
        return curr

class LibraryRulesAndRegulationAPI(generics.ListAPIView):
    serializer_class = LibraryRulesAndRegulationSerializer
    permission_classes = (AllowAny,)
    queryset = LibraryRulesAndRegulation.objects.filter(is_set = True)

class LibraryCommitteeAPI(generics.RetrieveAPIView):
    serializer_class = LibraryCommitteeSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        curr = LibraryCommittee.objects.get(is_current = True)
        return curr
    
class LibraryTeamAPI(generics.RetrieveAPIView):
    serializer_class = LibraryTeamSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        curr = LibraryTeam.objects.get(is_current = True)
        return curr

class FeedbackListAPI(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.filter(hidden = False)
    