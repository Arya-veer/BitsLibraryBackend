from rest_framework import serializers

from .models import UserProfile, Item, Claim


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        exclude = ('user','id')
