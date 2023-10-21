from rest_framework import views,generics
from rest_framework.permissions import AllowAny

from .serializers import *
# Create your views here.
class HomePageAPI(generics.RetrieveAPIView):
    serializer_class = HomePageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return HomePage.objects.get(is_set = True)
        except:
            return HomePage.objects.filter(is_set=True).order_by('-uploaded_on').first()