from rest_framework import serializers

from .models import Course, Paper

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '-' in data['name']:
            data['name'] = data['name'].split('-')[0].strip()
        return data
    
class PaperSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:
        model = Paper
        fields = '__all__'