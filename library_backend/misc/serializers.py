from rest_framework import serializers

from .models import *


class HomePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePage
        fields = "__all__"

class FreqAskedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreqAskedQuestion
        fields = "__all__"

    
class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"


class WebsiteTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebsiteText
        fields = ("title","text")