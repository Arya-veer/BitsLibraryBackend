from django.shortcuts import render
from rest_framework import generics
from .serializers import LinkClassSerializer,LinkClass,OpenETDsSerializer,OpenETDs

# Create your views here.


class ExternalLinksListAPI(generics.ListAPIView):
    authentication_classes = []
    serializer_class = LinkClassSerializer
    queryset = LinkClass.objects.filter(is_deleted = False)


class OpenETDsListAPI(generics.ListAPIView):
    authentication_classes = []
    serializer_class = OpenETDsSerializer
    queryset = OpenETDs.objects.all()