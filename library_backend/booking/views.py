from rest_framework import views,generics,viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *


class RoomListAPI(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RoomListSerializer
    queryset = Room.objects.all()


class RoomDetailAPI(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RoomDetailSerializer

    def get_serializer_context(self):
        return {'request':self.request,'date':self.request.query_params.get('date',None)}
    
    def get_object(self):
        return Room.objects.get(id = self.kwargs['id'])
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Room.DoesNotExist:
            return Response({"error":"Invalid room id"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        

class RoomVacancyCheckAPI(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,*args, **kwargs):
        if 'date' not in request.data:
            return Response({"error":"Date is not selected"},status=status.HTTP_400_BAD_REQUEST)
        if 'room' not in request.data:
            return Response({"error":"Room is not provided"},status=status.HTTP_400_BAD_REQUEST)
        booked_slot_ids = Booking.objects.filter(date = request.data['date'],roomslot__room__id = request.data['room'],status = "Approved").values_list('roomslot__slot',flat=True)
        booked_slots = SlotSerializer(Slot.objects.filter(id__in = booked_slot_ids),many=True).data
        free_slots = SlotSerializer(Slot.objects.exclude(id__in = booked_slot_ids),many=True).data
        return Response({"booked_slots":booked_slots,"free_slots":free_slots})
    

class BookRoomAPI(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args, **kwargs):
        if 'date' not in request.data:
            return Response({"error":"Date is not selected"},status=status.HTTP_400_BAD_REQUEST)
        if 'room' not in request.data:
            return Response({"error":"Room is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if 'slot' not in request.data:
            return Response({"error":"Slot is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if not 'no_of_participants' in request.data:
            return Response({"error":"Please give Number of participants"},status=status.HTTP_400_BAD_REQUEST)
        if request.user.profile.phone_number is None:
            return Response({"error":"Please update your phone number in profile before booking"},status=status.HTTP_400_BAD_REQUEST)
        if 'status' in request.data:
            request.data.pop('status')
        
        room =  request.data.pop('room')
        try:
            rs = RoomSlot.objects.get(room = room,slot =  request.data.pop('slot'))
        except RoomSlot.DoesNotExist:
            return Response({"error":"Room can not be booked for given slot"},status=status.HTTP_400_BAD_REQUEST)
        if Booking.objects.filter(date = request.data['date'],roomslot__room = room).exists():
            return Response({"error":"You have already applied for this room's booking! Check status on dashboard"},status=status.HTTP_400_BAD_REQUEST)
        if Booking.objects.filter(date = request.data['date'],status = "Approved",roomslot = rs).exists():
            return Response({"error":"This room is already booked at the selected time on selected date"},status=status.HTTP_400_BAD_REQUEST)
        try:
            Booking.objects.create(booker = request.user.profile,roomslot = rs,**request.data)
            return Response({"message":"Room has booked successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class BookingListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingListSerializer

    def get_queryset(self):
        return Booking.objects.filter(booker = self.request.user.profile)

class BookingDetailAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingDetailSerializer

    def get_object(self):

        booking = Booking.objects.get(id = self.kwargs['id'])
        if booking.booker != self.request.user.profile:
            raise Booking.DoesNotExist
        return booking
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Booking.DoesNotExist:
            return Response({"error":"Invalid booking id"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)

class BookingCancelAPI(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args, **kwargs):
        if 'id' not in request.data:
            return Response({"error":"Booking id is not provided"},status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id = request.data['id'])
            if booking.booker != request.user.profile:
                return Response({"error":"You are not authorized to cancel this booking"},status=status.HTTP_400_BAD_REQUEST)
            if booking.status in ["Cancelled","Rejected"]:
                return Response({"error":"This booking is already cancelled"},status=status.HTTP_400_BAD_REQUEST)
            booking.status = "Cancelled"
            booking.save()
            return Response({"message":"Booking has been cancelled successfully"},status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error":"Invalid booking id"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)