from rest_framework import serializers

from .models import *

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'

class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        exclude = ('campus',)