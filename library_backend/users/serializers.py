from rest_framework import serializers

from .models import UserProfile, Item, Claim


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
