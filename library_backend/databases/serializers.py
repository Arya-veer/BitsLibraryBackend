from rest_framework import serializers

from .models import *

import re

from django.db.models.functions import Length


class DatabaseSerializer(serializers.ModelSerializer):

    user_guide = serializers.SerializerMethodField()

    class Meta:
        model = Database
        exclude = ('campus','is_trial','user_guide_file','user_guide_url')
    

    def get_user_guide(self,obj):
        if obj.user_guide_file:
            return self.context['request'].build_absolute_uri(obj.user_guide_file.url)
        elif obj.user_guide_url:
            return obj.user_guide_url
        else:
            return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_trial:
            data['name'] = f"{data['name']} ({instance.campus.name})"
        return data

class CampusSerializer(serializers.ModelSerializer):

    databases = serializers.SerializerMethodField()

    class Meta:
        model = Campus
        fields = ('name','is_main','databases')
    
    def get_databases(self,obj):
        
        qs = Database.objects.filter(is_trial = False,campus = obj).order_by('name')
        return DatabaseSerializer(qs,many=True,context = self.context).data
    




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
        fields = ('name','author','publisher','subject','url','extra_data')
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        if 'isbn' in data['extra_data']:
            data['extra_data']['isbn'] = str(data['extra_data']['isbn'])
        if '.' in data['extra_data']['isbn']:
            data['extra_data']['isbn'] = data['extra_data']['isbn'].split('.')[0]
        if '/' in data['extra_data']['isbn']:
            data['extra_data']['isbn'] = data['extra_data']['isbn'].split('/')[0]
        if '-' in data['extra_data']['isbn']:
            data['extra_data']['isbn'] = data['extra_data']['isbn'].split('-')[0]
        # data['extra_data']['year'] = data['extra_data']['year'].split('.')[0]
        for key in data:
            if type(data.get(key)) == str and key in ['name']:
                data[key] = re.sub(r"[^a-zA-Z ]+","",(data[key]))
        # print(data)
        return data

class EJournalSerializer(serializers.ModelSerializer):
            
        publisher = PublisherSerializer()
        subject = SubjectSerializer()
        
        class Meta:
            model = EJournal
            fields = ('name','publisher','subject','url','extra_data')
        
        
        def to_representation(self, instance):
            data = super().to_representation(instance)
            for key in data:
                if type(data.get(key)) == str and key in ['name']:
                    data[key] = re.sub(r"[^a-zA-Z0-9 ]+","",(data[key]))
            # print(data)
            return data
        

class ELearningSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = ELearning
        fields = '__all__'

    def to_representation(self, instance):

        data = super().to_representation(instance)
        # print(data)
        return data


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        # fields = '__all__'
        exclude = ('user_guide_file','user_guide_url')
    

class DonatedBookSerializer(serializers.ModelSerializer):
    
    photo = serializers.SerializerMethodField()
    class Meta:
        model = DonatedBook
        # fields = '__all__'
        exclude = ("isbn","image")
    
    def get_photo(self,obj):
        if obj.isbn:
            return f"https://pictures.abebooks.com/isbn/{obj.isbn}-us-300.jpg"
        else:
            return self.context['request'].build_absolute_uri(obj.image.url)
    
class PublicationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Publication
        fields = '__all__'
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        for key in data:
            if type(data.get(key)) == str and key in ['title','authors','source_title']:
                data[key] = re.sub(r"[^a-zA-Z0-9 ]+","",(data[key]))
        # print(data)
        return data
    

    