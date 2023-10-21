from django.db import models,transaction
# Create your models here.
from datetime import timedelta

from users.models import UserProfile

from django.utils import timezone

class Facility(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField("Room Name",max_length=60,blank=True)
    capacity = models.IntegerField("Room Capacity",null=True)
    available_facilities = models.ManyToManyField(Facility) 

    def __str__(self) -> str:
        return self.name


class Slot(models.Model):    
    starttime = models.TimeField()
    endtime = models.TimeField()

    def __str__(self) -> str:
        return f"{self.starttime} - {self.endtime}"

class RoomSlot(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='roomslots')
    slot = models.ForeignKey(Slot,models.CASCADE,related_name='roomslots')

    def __str__(self) -> str:
        return f"{self.room} - {self.slot}"
    
    

class Booking(models.Model):

    booker = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='booked_rooms')
    status = models.CharField(max_length=40,choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'),('Cancelled','Cancelled')],default='Pending')
    date = models.DateField(default=timezone.now)
    roomslot = models.ForeignKey(RoomSlot,on_delete=models.CASCADE,related_name='bookings')
    requirements = models.JSONField(default=list)
    description = models.TextField(blank=True)
    no_of_participants = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.booker} - {self.status} - {self.roomslot}"
    
    def save(self,*args, **kwargs):
        if self.no_of_participants > self.roomslot.room.capacity:
            raise Exception(f"Only {self.roomslot.room.capacity} participants are allowed")
        if Booking.objects.filter(date = self.date,booker = self.booker,roomslot__room = self.roomslot.room).exists():
            raise Exception(f"You have already booked {self.roomslot.room} for {self.roomslot.slot} slot today")
        if Booking.objects.filter(date = self.date,roomslot = self.roomslot).exists():
            raise Exception(f"{self.roomslot.room} has already been booked for the slot {self.roomslot.slot} on date {self.date}")
        if not (set(self.requirements).issubset(set(self.roomslot.room.available_facilities.values_list().distinct()))):
            raise Exception("Facilities are not matching room")
        super().save(*args, **kwargs)


