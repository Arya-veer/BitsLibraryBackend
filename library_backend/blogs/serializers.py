from rest_framework import serializers

from .models import *

import re

from django.db.models.functions import Length

class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = '__all__'
        
class BlogHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id','title','image','published_date', 'archived')