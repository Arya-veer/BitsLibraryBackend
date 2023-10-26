from .models import *

from rest_framework import serializers


    
class ExternalLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkSite
        fields = '__all__'

class InflibnetLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = InflibnetLink
        fields = '__all__'