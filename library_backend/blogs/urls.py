from django.urls import path

from rest_framework.routers import SimpleRouter
from django.urls import include
from .views import *


urlpatterns = []

blog_router = SimpleRouter()

blog_router.register(r'',BlogViewSet)

urlpatterns += [path("", include(blog_router.urls))]
