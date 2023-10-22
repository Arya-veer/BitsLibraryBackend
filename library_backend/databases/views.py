from rest_framework import views,generics,status,response

from .serializers import *
# Create your views here.


class CampusListAPI(generics.ListAPIView):
    serializer_class = CampusSerializer
    queryset = Campus.objects.filter(is_main = False)


class DatabaseListAPI(generics.ListAPIView):
    serializer_class = DatabaseSerializer
    
    def get_queryset(self):
        qs = Database.objects.all()
        campus = self.request.query_params.get('campus',None)
        if campus is None:
            qs.filter(campus__is_main = True)
        else:
            qs.filter(campus__id = campus)
        return qs