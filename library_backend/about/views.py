
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
            return LibraryTeam.objects.get(description = "Pilani")        
        return LibraryTeam.objects.get(description = f"{self.request.query_params['campus']}")



class LibraryBrochureAPI(generics.RetrieveAPIView):
    serializer_class = LibraryBrochureSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return LibraryBrochure.objects.get(is_set = True)
        except:
            return LibraryBrochure.objects.filter(is_set=True).order_by('-uploaded_on').first()
        
class LibraryWebsiteUserGuideAPI(generics.RetrieveAPIView):
    serializer_class = LibraryWebsiteUserGuideSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return LibraryWebsiteUserGuide.objects.get(is_set = True)
        except:
            return LibraryWebsiteUserGuide.objects.filter(is_set=True).order_by('-uploaded_on').first()
class LibraryCalendarsAPI(generics.RetrieveAPIView):
    serializer_class = LibraryCalendarsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return LibraryCalendar.objects.get(is_set = True)
        except:
            return LibraryCalendar.objects.filter(is_set=True).order_by('-uploaded_on').first()


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
    queryset = Event.objects.filter(is_set = True).order_by('-date','-time')
    # ordering = ['-date','-time']

class NewsAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_set = True).order_by('-date')
    # ordering = ['-date']

class BookMarqueeAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookMarqueeSerializer
    queryset = BookMarquee.objects.filter(is_set = True)


class LibraryTimingsAPI(views.APIView):


    def get(self,request):
        current_date = timezone.now().date()
        timings = LibraryTiming.objects.filter(startdate__lte = current_date,enddate__gte = current_date)
        if timings.exists():
            return Response(LibraryTimingSerializer(timings.first(),context = {"timings":True}).data,status=status.HTTP_200_OK)
        current_day = current_date.weekday()
        timings = LibraryTiming.objects.filter(startdate__week_day = current_day)
        if timings.exists():
            return Response(LibraryTimingSerializer(timings.first(),context = {"timings":True}).data,status=status.HTTP_200_OK)
        lt_dummy = LibraryTiming(startdate = current_date,enddate = current_date,opening_time = "00:00:00",closing_time = "00:00:00")
        return Response(LibraryTimingSerializer(lt_dummy,context = {"timings":False}).data,status=status.HTTP_200_OK)  
