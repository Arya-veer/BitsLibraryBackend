from rest_framework import serializers

from .models import *


class HomePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePage
        fields = "__all__"