from django.shortcuts import render
from rest_framework import generics
from .serializers import *

# Create your views here.


class ExternalLinksListAPI(generics.ListAPIView):
    authentication_classes = []
    serializer_class = ExternalLinkSerializer
    
    def get_queryset(self):
        link_type = self.request.query_params.get('link_type',None)
        links = LinkSite.objects.all().order_by("site_name")
        if link_type is not None:
            return links.filter(link_type = link_type)

