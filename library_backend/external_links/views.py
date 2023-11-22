from django.shortcuts import render
from rest_framework import generics
from .serializers import *

from databases.serializers import ELearning,ELearningSerializer,OpenAccess

# Create your views here.


class ExternalLinksListAPI(generics.ListAPIView):
    authentication_classes = []
    # serializer_class = ExternalLinkSerializer
    def get_serializer_class(self):
        link_type = self.request.query_params.get('link_type',None)
        if link_type == "E-Learning":
            return ELearningSerializer
        elif link_type == "Platform":
            return PlatformSerializer
        elif link_type == "OpenAccess":
                return OpenAccessSerializer
        elif link_type == "NewArrival":
            return NewArrivalSerializer
        else:
            return ExternalLinkSerializer

    
    def get_queryset(self):
        link_type = self.request.query_params.get('link_type',None)
        links = LinkSite.objects.all().order_by("site_name")
        if link_type is not None:
            if link_type == "E-Learning":
                links = ELearning.objects.all().order_by("site_name")
            elif link_type == "Platform":
                links = Platform.objects.all().order_by("name")
            elif link_type == "OpenAccess":
                links = OpenAccess.objects.all().order_by("name")
            elif link_type == "NewArrival":
                links = NewArrival.objects.all().order_by("-year",)
            else:
                links = links.filter(link_type = link_type)
        return links

