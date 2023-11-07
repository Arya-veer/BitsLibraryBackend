from .models import *
from databases.models import Platform,OpenAccess
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
    site_type = serializers.SerializerMethodField()

    class Meta:
        model = OpenAccess
        fields = ('site_name','url','image','site_type')

    def get_image(self,obj):
        return None

    def get_site_type(self,obj):
        return "Open Access"

class InflibnetLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = InflibnetLink
        fields = '__all__'