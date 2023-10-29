from django.shortcuts import render
from rest_framework import generics
from .serializers import *

from databases.serializers import ELearning,ELearningSerializer

# Create your views here.


class ExternalLinksListAPI(generics.ListAPIView):
    authentication_classes = []
    # serializer_class = ExternalLinkSerializer
    def get_serializer_class(self):
        link_type = self.request.query_params.get('link_type',None)
        if link_type == "E-Learning":
            return ELearningSerializer
        else:
            return ExternalLinkSerializer

    
    def get_queryset(self):
        link_type = self.request.query_params.get('link_type',None)
        links = LinkSite.objects.all().order_by("site_name")
        if link_type is not None:
            if link_type == "E-Learning":
                links = ELearning.objects.all().order_by("site_name")
            else:
                links = links.filter(link_type = link_type)
        return links

