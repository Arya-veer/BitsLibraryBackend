from rest_framework import views,generics,viewsets,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

from library_backend import keyconfig as senv

from users.permissions import StaffPermission

import datetime

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
            print(str(e))
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

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

    @csrf_exempt
    def post(self,request):
        requirements = request.data.getlist('requirements')
        data = request.data.dict()
        # print(data)
        new_data = {key:val for key,val in data.items() if key in ['date','room','slot','requirements','no_of_participants','description','phone_number']}
        data = new_data
        data['requirements'] = requirements
        print(data)
        if 'date' not in data:
            return Response({"error":"Date is not selected"},status=status.HTTP_400_BAD_REQUEST)
        date = datetime.datetime.strptime(data['date'],"%Y-%m-%d").date()
        # Check if date is not today tomorrow or day after tomorrow
        if date < datetime.date.today() or date > datetime.date.today() + datetime.timedelta(days=2):
            return Response({"error":"You can only book room for today, tomorrow or day after tomorrow"},status=status.HTTP_400_BAD_REQUEST)
        if 'room' not in data or not  data['room']:
            return Response({"error":"Room is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if 'slot' not in data or not data['slot']:
            return Response({"error":"Slot is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if 'no_of_participants' not in data or not data['no_of_participants']:
            return Response({"error":"Please give Number of participants"},status=status.HTTP_400_BAD_REQUEST)
        data['no_of_participants'] = int(data['no_of_participants'])
        if request.user.profile.phone_number is None:
            if 'phone_number' in data:
                request.user.profile.phone_number = data.pop('phone_number')
                request.user.profile.save()
            else:
                return Response({"error":"Please update your phone number in profile before booking"},status=status.HTTP_400_BAD_REQUEST)
        if 'status' in data:
            data.pop('status')
            return Response({"error":"You can not set status of booking! You have been reported for sem back"},status=status.HTTP_400_BAD_REQUEST)
        
        room =  data.pop('room')
        try:
            rs = RoomSlot.objects.get(room = room,slot =  data.pop('slot'))
        except RoomSlot.DoesNotExist:
            return Response({"error":"Room can not be booked for given slot"},status=status.HTTP_400_BAD_REQUEST)
        if rs.room.is_closed:
            return Response({"error":"This room not available for booking"},status=status.HTTP_400_BAD_REQUEST)
        try:
            if Booking.objects.filter(date = data['date'],booker = request.user.profile,roomslot__room = room,status__in = ["Pending","Approved"]).exists():
                return Response({"error":"You have already applied for this room's booking! Check status on dashboard"},status=status.HTTP_400_BAD_REQUEST)
            if Booking.objects.filter(date = data['date'],roomslot = rs,status__in = ["Approved","Pending"]).exists():
                return Response({"error":"This room is already booked at the selected time on selected date"},status=status.HTTP_400_BAD_REQUEST)
            requirements = data.pop('requirements')
            if type(requirements) == list:
                data['requirements'] = requirements
            elif type(requirements) == str:
                data['requirements'] = [requirements]
            else:
                return Response({"error":"Invalid requirements"},status=status.HTTP_400_BAD_REQUEST)
            Booking.objects.create(booker = request.user.profile,roomslot = rs,**data)
            return Response({"message":"Request sent for room booking"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class TestBookingAPI(views.APIView):

    permission_classes = (AllowAny,)

    def post(self,request):
        if 'key' not in request.data:
            return Response({"error":"Key is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['key'] != senv.API_KEY:
            return Response({"error":"Invalid key"},status=status.HTTP_400_BAD_REQUEST)
        if 'date' not in request.data:
            return Response({"error":"Date is not selected"},status=status.HTTP_400_BAD_REQUEST)
        if 'room' not in request.data:
            return Response({"error":"Room is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if 'slot' not in request.data:
            return Response({"error":"Slot is not provided"},status=status.HTTP_400_BAD_REQUEST)
        rs = RoomSlot.objects.get(room = request.data['room'],slot = request.data['slot'])
        if 'uid' not in request.data:
            return Response({"error":"UID is not provided"},status=status.HTTP_400_BAD_REQUEST)
        booking = Booking.objects.filter(date = request.data['date'],status = "Approved",roomslot = rs)
        if booking.exists():
            booking.update(status = "Cancelled")
        Booking.objects.create(booker = UserProfile.objects.get(uid = request.data.get('uid')),roomslot = rs,date = request.data['date'],no_of_participants = rs.room.max_capacity)  
        return Response({"message":"Booking has been done successfully"},status=status.HTTP_200_OK)    




class BookingListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingListSerializer

    def get_queryset(self):
        bookings = Booking.objects.filter(booker = self.request.user.profile).order_by('-date')
        if 'upcoming' in self.request.query_params:
            bookings = bookings.filter(date__gte = datetime.date.today())
        return bookings

class BookingDetailAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingDetailSerializer

    def get_object(self):

        booking = Booking.objects.get(id = self.kwargs['id'])
        if booking.booker.user_type != "Staff" and booking.booker != self.request.user.profile:
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
            data = request.data.dict()
            # print(data)
            new_data = {key:val for key,val in data.items() if key == 'id'}
            data = new_data
            booking = Booking.objects.get(id = request.data['id'])
            if booking.booker != request.user.profile:
                return Response({"error":"You are not authorized to cancel this booking"},status=status.HTTP_400_BAD_REQUEST)
            if booking.status in ["Cancelled","Rejected"]:
                return Response({"error":"This booking is already cancelled"},status=status.HTTP_400_BAD_REQUEST)
            if booking.date < datetime.date.today():
                return Response({"error":"You can not cancel booking after the date has passed"},status=status.HTTP_400_BAD_REQUEST)
            if booking.date == datetime.date.today() and booking.roomslot.slot.starttime < datetime.datetime.now().time():
                return Response({"error":"You can not cancel booking after the slot has started"},status=status.HTTP_400_BAD_REQUEST)
            booking.status = "Cancelled"
            booking.save()
            return Response({"message":"Booking has been cancelled successfully"},status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error":"Invalid booking id"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class StaffBookingListAPI(generics.ListAPIView):
    permission_classes = (StaffPermission,)
    serializer_class = BookingListSerializer
    
    def get_queryset(self):
        bookings = Booking.objects.all()
        if 'type' in self.request.query_params:
            booking_type = self.request.query_params['type']
            if booking_type == "Pending":
                bookings = Booking.objects.filter(status = "Pending",date__gte = datetime.date.today())
            elif booking_type == "Processed":
                bookings = Booking.objects.filter(status__in = ["Approved","Rejected"],date__gte = datetime.date.today())
            elif booking_type == "Past":
                bookings = Booking.objects.filter(date__lt = datetime.date.today()) | Booking.objects.filter(date = datetime.date.today())
            else:
                raise Exception("Invalid booking type")
        return bookings.order_by('-date')
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class BookingApproveRejectAPI(views.APIView):
    permission_classes = (StaffPermission,)
    
    def post(self,request,*args, **kwargs):
        booking = Booking.objects.filter(id = request.data.get('id',-1)).first()
        if not booking:
            return Response({"error":"Booking not found"},status=status.HTTP_400_BAD_REQUEST)
        if booking.status not in ["Pending","Rejected"]:
            return Response({"error":"Booking is already approved or cancelled"},status=status.HTTP_400_BAD_REQUEST)
        if 'status' not in request.data:
            return Response({"error":"Status is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['status'] not in ["Approved","Rejected"]:
            return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['status'] == "Rejected" and 'rejection_reason' not in request.data:
            return Response({"error":"Rejection reason is not provided"},status=status.HTTP_400_BAD_REQUEST)
        if request.data['status'] == "Rejected":
            booking.rejection_reason = request.data['rejection_reason']
        booking.status = request.data['status']
        booking.save()
        return Response({"message":f"Booking has been {status.lower()}"},status=status.HTTP_200_OK)
        
    