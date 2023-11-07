from .models import *
from databases.models import Platform,OpenAccess,NewArrival
from rest_framework import serializers


    
class ExternalLinkSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = LinkSite
        fields = ('site_name','url','image','site_type')

    def get_url(self,obj):
        request = self.context['request']
        if obj.link_type == "Download Form":
            return request.build_absolute_uri(obj.file.url)
        else:
            return obj.url
        
class PlatformSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="name")
    url = serializers.CharField(source="link")
    # image = serializers.ImageField(source="image")
    site_type = serializers.CharField(source="campus.name")

    class Meta:
        model = Platform
        fields = ('site_name','url','image','site_type')

class OpenAccessSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="name")
    url = serializers.CharField(source="link")
    image = serializers.SerializerMethodField()
    # site_type = serializers.SerializerMethodField()

    class Meta:
        model = OpenAccess
        fields = ('site_name','url','image',)

    def get_image(self,obj):
        return None
    
class NewArrivalSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source="month")
    url = serializers.FileField(source="file")
    site_type = serializers.CharField(source="year")
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewArrival
        fields = ('site_name','url','site_type','image',)

    def get_image(self,obj):
        return None


class InflibnetLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = InflibnetLink
        fields = '__all__'