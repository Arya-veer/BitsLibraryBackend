from rest_framework import serializers

from .models import *


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        exclude = ('campus',)


class CampusSerializer(serializers.ModelSerializer):

    databases = serializers.SerializerMethodField()

    class Meta:
        model = Campus
        fields = ('name','is_main','databases')
    
    def get_databases(self,obj):
        
        qs = Database.objects.filter(is_trial = False,campus = obj).order_by("name")
        return DatabaseSerializer(qs,many=True).data

