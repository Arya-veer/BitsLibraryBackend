from .models import *

from rest_framework import serializers


    
class ExternalLinkSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = LinkSite
        fields = ('site_name','url','link_type','image')

    def get_url(self,obj):
        if obj.link_type == "Download Form":
            return obj.file.url
        else:
            return obj.url

class InflibnetLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = InflibnetLink
        fields = '__all__'