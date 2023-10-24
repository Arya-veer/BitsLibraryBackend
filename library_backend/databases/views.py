from rest_framework import views,generics,status,response,pagination

from .serializers import *
# Create your views here.


class CampusListAPI(generics.ListAPIView):
    serializer_class = CampusSerializer
    queryset = Campus.objects.all()

class TrialDatabaseListAPI(generics.ListAPIView):
    serializer_class = DatabaseSerializer
    queryset = Database.objects.filter(is_trial=True)


class PublisherListAPI(generics.ListAPIView):
    serializer_class = PublisherSerializer
    
    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        queryset = Publisher.objects.all()
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('name')


class EBookListAPI(generics.ListAPIView):
    serializer_class = EBookSerializer

    class EBookPagination(pagination.PageNumberPagination):
        page_size = 10

    pagination_class = EBookPagination

    def get_queryset(self):
        queryset = EBook.objects.all()
        publisher = self.request.query_params.get('publisher', None)
        search = self.request.query_params.get('search', None)
        if publisher is not None:
            queryset = queryset.filter(publisher__name=publisher)
        if search is not None:
            sub = Subject.objects.filter(name__icontains=search)
            if sub.exists():
                queryset = queryset.filter(subject=sub[0])
            queryset |= queryset.filter(name__icontains=search) | queryset.filter(author__icontains=search) | queryset.filter(description__icontains=search) | queryset.filter(url__icontains=search) 
        return queryset