from rest_framework import serializers

from .models import *

import datetime

class FacilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Facility
        fields = "__all__"

class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ['available_facilities',]
    
class SlotSerializer(serializers.ModelSerializer):

    is_booked = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = "__all__"
    
    def get_is_booked(self,obj):
        if self.context.get('date') and self.context.get('room'):
            return obj.id in Booking.objects.filter(date = self.context['date'],roomslot__room = self.context['room'],status = "Approved").values_list('roomslot__slot',flat=True).distinct()
        return False

class RoomDetailSerializer(serializers.ModelSerializer):

    slots = serializers.SerializerMethodField()
    user_has_phone_number = serializers.SerializerMethodField()
    available_facilities = FacilitySerializer(many=True)

    class Meta:
        model = Room
        fields = ('id','name','min_capacity','max_capacity','slots','available_facilities','image','description','user_has_phone_number')
    
    def get_slots(self,obj):
        qs = Slot.objects.filter(id__in = obj.roomslots.all().values_list('slot',flat=True).distinct())
        self.context['room'] = obj
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        day_after_tomorrow = today + datetime.timedelta(days=2)
        # if user has booking on given date then return true else return false


        data = {
            str(today):{
                'slots':SlotSerializer(qs,many=True,context={'date':today,'room':obj}).data,
                'user_has_booking':Booking.objects.filter(date = today,roomslot__room = obj,booker = self.context.get("request").user.profile,status__in = ["Pending","Approved"]).exists()
            }  ,
            str(tomorrow):{
                'slots':SlotSerializer(qs,many=True,context={'date':tomorrow,'room':obj}).data,
                'user_has_booking':Booking.objects.filter(date = tomorrow,roomslot__room = obj,booker = self.context.get("request").user.profile,status__in = ["Pending","Approved"]).exists()
            },
            str(day_after_tomorrow):{
                'slots':SlotSerializer(qs,many=True,context={'date':day_after_tomorrow,'room':obj}).data,
                'user_has_booking':Booking.objects.filter(date = day_after_tomorrow,roomslot__room = obj,booker = self.context.get("request").user.profile,status__in = ["Pending","Approved"]).exists()
            }
        }
        # print(data)
        return data
    
    def get_user_has_phone_number(self,obj):
        return self.context['request'].user.profile.phone_number is not None
    
class BookingListSerializer(serializers.ModelSerializer):

    room = serializers.CharField(source = 'roomslot.room.name')
    slot = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id','status','date','room','slot','no_of_participants')

    def get_slot(self,obj):
        return f"{obj.roomslot.slot.starttime} - {obj.roomslot.slot.endtime}"

class BookingDetailSerializer(BookingListSerializer):

    class Meta:
        model = Booking
        fields = BookingListSerializer.Meta.fields + ('requirements','description')