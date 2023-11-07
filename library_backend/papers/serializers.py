from rest_framework import serializers

from .models import Course, Paper, TextBook

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(self.context)
        if '-' in data['name']:
            data['name'] = data['name'].split('-')[0].strip()
        return data
    
class PaperSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:
        model = Paper
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '-' in instance.course.name:
            data['type'] = instance.course.name.split('-')[1].strip()
        else: 
            data['type'] = 'Comprehensive'
        
        return data
    

class TextBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextBook
        exclude = ('course','id')
    