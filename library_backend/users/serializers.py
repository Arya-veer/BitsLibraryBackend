from rest_framework import serializers

from .models import UserProfile, Item, Claim, ArticleBookRequest


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('auth_user','id')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    class Meta:
        model = Claim
        exclude = ('user','id')

class ArticleBookRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleBookRequest
        exclude = ('user','id')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user.profile
        return super().create(validated_data)