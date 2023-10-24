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


class PublisherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Publisher
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Subject
        fields = "__all__"

class EBookSerializer(serializers.ModelSerializer):
        
    publisher = PublisherSerializer()
    subject = SubjectSerializer()
    
    class Meta:
        model = EBook
        fields = ('name','author','publisher','subject','description','url','extra_data')
    
    