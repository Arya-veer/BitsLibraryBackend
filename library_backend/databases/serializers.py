from rest_framework import serializers

from .models import *

import re

from django.db.models.functions import Length


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        exclude = ('campus','is_trial')


class CampusSerializer(serializers.ModelSerializer):

    databases = serializers.SerializerMethodField()

    class Meta:
        model = Campus
        fields = ('name','is_main','databases')
    
    def get_databases(self,obj):
        
        qs = Database.objects.filter(is_trial = False,campus = obj).order_by(Length("description").asc(),'name')
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
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['extra_data']['isbn'] = data['extra_data']['isbn'].split('.')[0]
        data['extra_data']['year'] = data['extra_data']['year'].split('.')[0]
        for key in data:
            if type(data.get(key)) == str:
                data[key] = re.sub(r"[^a-zA-Z ]+","",(data[key]))
        # print(data)
        return data