from rest_framework import serializers

from .models import UserProfile, Item, Claim, ArticleBookRequest,FreeBook,FreeBookPick


class UserProfileSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(source='auth_user.email',read_only=True)
    class Meta:
        model = UserProfile
        exclude = ('auth_user','id')

class ItemSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField(read_only = True)
    dt = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Item
        fields = '__all__'

    def get_dt(self,obj):
        return obj.dt.strftime("%d/%m/%Y %I:%M %p")

    def get_status(self,obj):
        profile = self.context['request'].user.profile
        if profile.claims.filter(item=obj,status="Approved").exists():
            return "Approved"
        elif profile.claims.filter(item=obj,status="Pending").exists():
            if Claim.objects.filter(item = obj,status = "Approved").exists():
                return "Rejected"
            else:
                return "Pending"
        if Claim.objects.filter(item = obj,status = "Approved").exists():
            return "Someone else claimed"
        else:
            return "Not Claimed"

class StaffItemSerializer(serializers.ModelSerializer):
    
    claimed_by = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'
    
    def get_claimed_by(self,obj):
        if obj.claims.filter(status="Approved").exists():
            return UserProfileSerializer(obj.claims.filter(status="Approved").first().user).data
        return None
        
        
            

class ClaimSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    class Meta:
        model = Claim
        exclude = ('user','id')
        
class StaffClaimSerializer(serializers.ModelSerializer):
    
    user = UserProfileSerializer()
    
    class Meta:
        model = Claim
        exclude = ('item',)

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

class ArticleBookRequestStaffSerializer(serializers.ModelSerializer):
    # status = serializers.SerializerMethodField()
    class Meta:
        model = ArticleBookRequest
        fields = '__all__'

    # def get_status(self,obj):
    #     profile = self._context['request'].user.profile
    #     applications = profile.article_book_requests.filter(book=obj)
    #     if applications.exists():
    #         applications = applications.first()
    #         return applications.status
    #     elif ArticleBookRequest.objects.filter(book=obj,status="Approved").exists():
    #         return "Already Requested"
    #     else:
    #         return "Not Requested"

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
    
class StaffFreeBookSerializer(serializers.ModelSerializer):
    
    claimed_by = serializers.SerializerMethodField()
    class Meta:
        model = FreeBook
        fields = '__all__'
    
    def get_claimed_by(self,obj):
        if obj.free_book_picks.filter(status='Approved').exists():
            return UserProfileSerializer(obj.free_book_picks.filter(status='Approved').first().user).data
        return None
    
class StaffFreeBookPickSerializer(serializers.ModelSerializer):
    
    user = UserProfileSerializer()
    
    class Meta:
        model = FreeBookPick
        exclude = ('book',)
