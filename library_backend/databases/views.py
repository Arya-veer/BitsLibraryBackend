from rest_framework import views,generics,status,response,pagination

from .serializers import *

# Create your views here.

class CampusListAPI(generics.ListAPIView):
    serializer_class = CampusSerializer
    queryset = Campus.objects.all().order_by('-is_main','name')

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        # print(data)
        trial_databases = DatabaseSerializer(Database.objects.filter(is_trial = True),many=True,context = self.get_serializer_context()).data
        data.append(
            {
                "name":"Trial Databases",
                "is_main":False,
                "databases":trial_databases
            }
        )
        return response.Response(data)


class PublisherListAPI(generics.ListAPIView):
    serializer_class = PublisherSerializer

    class PublisherPagination(pagination.PageNumberPagination):
        page_size = 50
    
    pagination_class = PublisherPagination
    
    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        queryset = Publisher.objects.all()
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('name')


class EBookListAPI(generics.ListAPIView):
    serializer_class = EBookSerializer

    class EBookPagination(pagination.PageNumberPagination):
        page_size = 20

    pagination_class = EBookPagination

    def get_queryset(self):
        queryset = EBook.objects.all().order_by('id')
        search = self.request.query_params.get('search', None)
        print(search)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(author__icontains=search) | queryset.filter(url__icontains=search) | queryset.filter(publisher__name__icontains=search) | queryset.filter(subject__name__icontains=search)
        return queryset
    
class EJournalListAPI(generics.ListAPIView):
    serializer_class = EJournalSerializer

    class EJournalPagination(pagination.PageNumberPagination):
        page_size = 20

    pagination_class = EJournalPagination

    def get_queryset(self):
        queryset = EJournal.objects.all().order_by('name')
        queryset = queryset.exclude(name='')

        search = self.request.query_params.get('search', None)
        print(search)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(url__icontains=search) | queryset.filter(publisher__name__icontains=search) | queryset.filter(subject__name__icontains=search)
        return queryset



class PlatformListAPI(generics.ListAPIView):
    serializer_class = PlatformSerializer
    queryset = Platform.objects.filter(campus__name = "Pilani")

class DonatedBookListAPI(generics.ListAPIView):

    serializer_class = DonatedBookSerializer
    # queryset = DonatedBook.objects.all().order_by('isbn')

    def get_queryset(self):
        if "book_type" in self.request.query_params:
            return DonatedBook.objects.filter(book_type = self.request.query_params['book_type']).order_by('isbn')
        return DonatedBook.objects.filter(book_type = "DonatedBook").order_by('isbn')