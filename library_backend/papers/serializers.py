from rest_framework import serializers

from .models import Course, Paper

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    
class PaperSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:
        model = Paper
        fields = '__all__'