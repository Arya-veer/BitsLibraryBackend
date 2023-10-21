from rest_framework import serializers

from .models import *

class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ['available_facilities',]
    
class SlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slot
        fields = "__all__"

class RoomDetailSerializer(serializers.ModelSerializer):

    slots = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id','name','capacity','slots','available_facilities')
    
    def get_slots(self,obj):
        qs = Slot.objects.filter(id__in = obj.roomslots.all().values_list('slot',flat=True).distinct())
        if self.context.get('user') and self.context.get('date'):
            qs = qs.exclude(id__in = Booking.objects.filter(date = self.context['date'],roomslot__room = obj).values_list('roomslot__slot',flat=True).distinct())
        return SlotSerializer(qs,many=True).data
    
class BookingListSerializer(serializers.ModelSerializer):

    room = serializers.SerializerMethodField()
    slot = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id','status','date','room','slot','no_of_participants')

    def get_room(self,obj):
        return obj.roomslot.room.name
    
    def get_slot(self,obj):
        return f"{obj.roomslot.slot.starttime} - {obj.roomslot.slot.endtime}"

class BookingDetailSerializer(BookingListSerializer):

    class Meta:
        model = Booking
        fields = BookingListSerializer.Meta.fields + ('requirements','description')