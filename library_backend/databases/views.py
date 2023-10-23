from rest_framework import views,generics,status,response

from .serializers import *
# Create your views here.


class CampusListAPI(generics.ListAPIView):
    serializer_class = CampusSerializer
    queryset = Campus.objects.all()

class TrialDatabaseListAPI(generics.ListAPIView):
    serializer_class = DatabaseSerializer
    queryset = Database.objects.filter(is_trial=True)