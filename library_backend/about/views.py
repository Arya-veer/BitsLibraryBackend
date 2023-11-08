
from rest_framework import views,generics,status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
        if 'campus' not in self.request.query_params:
            return LibraryTeam.objects.get(description = "Pilani Team")        
        return LibraryTeam.objects.get(description = f"{self.request.query_params['campus']} Team")



class LibraryBrochureAPI(generics.RetrieveAPIView):
    serializer_class = LibraryBrochureSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return LibraryBrochure.objects.get(is_set = True)
        except:
            return LibraryBrochure.objects.filter(is_set=True).order_by('-uploaded_on').first()
        
class LibraryTimingsAPI(generics.RetrieveAPIView):
    serializer_class = LibraryTimingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return LibraryTiming.objects.get(is_set = True)
        except:
            return LibraryTiming.objects.filter(is_set=True).order_by('-uploaded_on').first()


class LibrarianDeskAPI(views.APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        librarian = LibraryTeamMember.objects.filter(is_librarian = True).first()
        if librarian:
            return Response(LibraryTeamMemberSerializer(librarian).data)
        else:
            return Response({"error":"No Librarian right now"},status=status.HTTP_404_NOT_FOUND)


class EventListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.filter(is_set = True)

class NewsAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_set = True)

class BookMarqueeAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookMarqueeSerializer
    queryset = BookMarquee.objects.filter(is_set = True)