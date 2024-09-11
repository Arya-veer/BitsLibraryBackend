from rest_framework import views,generics,status,response,pagination

from .serializers import *
from rest_framework import viewsets

from users.permissions import AdminPermission

# Create your views here.
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-published_date')
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ['create','update','partial_update','destroy']:
            permission_classes = [AdminPermission]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogHeaderSerializer
        return BlogSerializer