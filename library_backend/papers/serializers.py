from rest_framework import serializers

from .models import Course, Paper, TextBook

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    
class PaperSerializer(serializers.ModelSerializer):

    course = CourseSerializer()
    class Meta:
        model = Paper
        fields = '__all__'
    


class TextBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextBook
        exclude = ('course','id')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'year' in data['extra_data'] and '.' in data['extra_data']['year']:
            data['extra_data']['year'] = data['extra_data']['year'].split('.')[0]
        return data
    