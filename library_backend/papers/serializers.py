from rest_framework import serializers

from .models import Course, Paper

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '-' in data['name'] and self.context['split']:
            data['name'] = data['name'].split('-')[0].strip()
        return data
    
class PaperSerializer(serializers.ModelSerializer):

    course = CourseSerializer(context = {'split':False})
    class Meta:
        model = Paper
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '-' in data['course']['name']:
            data['type'] = data['course']['name'].split('-')[1].strip()
            data['course']['name'] = data['course']['name'].split('-')[0].strip()
        else: 
            data['type'] = 'Comprehensive'
        
        return data