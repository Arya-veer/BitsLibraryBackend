from .models import *

from rest_framework import serializers


    
class LinkSiteSerializer(serializers.ModelSerializer):


    class Meta:
        model = LinkSite
        exclude = ["link_class"]
    


class LinkClassSerializer(serializers.ModelSerializer):

    sites = LinkSiteSerializer(many = True)

    class Meta:
        model = LinkClass
        fields = "__all__"

