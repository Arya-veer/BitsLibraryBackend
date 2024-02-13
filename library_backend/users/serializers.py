from rest_framework import serializers

from .models import UserProfile, Item, Claim, ArticleBookRequest,FreeBook,FreeBookPick


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('auth_user','id')

class ItemSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    dt = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'

    def get_dt(self,obj):
        return obj.dt.strftime("%d/%m/%Y %I:%M %p")

    def get_status(self,obj):
        profile = self.context['request'].user.profile
        if profile.claims.filter(item=obj,is_approved=True).exists():
            return "Approved"
        elif profile.claims.filter(item=obj,is_approved=False).exists():
            return "Pending"
        elif Claim.objects.filter(item = obj,is_approved = True).exists():
            return "Someone else claimed"
        else:
            return "Not Claimed"

class StaffItemSerializer(serializers.ModelSerializer):
    
    claimed_by = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'
    
    def get_claimed_by(self,obj):
        if obj.claims.filter(is_approved=True).exists():
            return UserProfileSerializer(obj.claims.filter(is_approved=True).first()).data
        return None
        
        
            

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
        if 'status' in validated_data:
            validated_data.pop('status')
        return super().create(validated_data)


class FreeBookSerialzer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    class Meta:
        model = FreeBook
        fields = '__all__'

    def get_status(self,obj):
        profile = self.context['request'].user.profile
        applications = profile.free_book_picks.filter(book=obj)
        if applications.exists():
            application = applications.first()
            return application.status
        elif FreeBookPick.objects.filter(book=obj,status="Approved").exists():
            return "Already Picked"
        else:
            return "Not Picked"

class FreeBookPickSerializer(serializers.ModelSerializer):
    book = FreeBookSerialzer()

    class Meta:
        model = FreeBookPick
        exclude = ('user','id')
    