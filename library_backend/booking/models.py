from typing import Any
from django.db import models,transaction
# Create your models here.
from datetime import timedelta,datetime
from misc.models import AbstractBaseModel

from users.models import UserProfile

from django.utils import timezone

class Facility(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    cost_per_minute = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField("Room Name",max_length=60,blank=True)
    min_capacity = models.IntegerField("Min Room Capacity",null=True)
    max_capacity = models.IntegerField("Max Room Capacity",null=True)
    available_facilities = models.ManyToManyField(Facility)
    image = models.ImageField(null=True,upload_to='room_images')
    description = models.TextField(blank=True)


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
    
    class Meta:
        unique_together = ['room','slot']
        verbose_name = "Room Slot"
        verbose_name_plural = "Room Slots"

class Booking(models.Model):

    booker = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='booked_rooms')
    status = models.CharField(max_length=40,choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'),('Cancelled','Cancelled')],default='Pending')
    date = models.DateField(default=timezone.now)
    roomslot = models.ForeignKey(RoomSlot,on_delete=models.CASCADE,related_name='bookings')
    requirements = models.JSONField(default=list,blank=True)
    description = models.TextField(blank=True)
    no_of_participants = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.booker} - {self.status} - {self.roomslot}"
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.prev_status = self.status
    
    def get_amount(self):
        """Gets difference of start and end time in minutes and multiplies it with cost per minute of each facility from requirements"""
        total_cost_per_minute = 0
        minutes = (datetime.combine(datetime.today(),self.roomslot.slot.endtime) - datetime.combine(datetime.today(),self.roomslot.slot.starttime)).total_seconds()/60
        for facility in self.requirements:
            total_cost_per_minute += Facility.objects.get(name = facility).cost_per_minute
        return total_cost_per_minute * minutes
    
    def save(self,*args, **kwargs):
        if self._state.adding:
            if self.no_of_participants > self.roomslot.room.max_capacity:
                raise Exception(f"Maximum {self.roomslot.room.max_capacity} participants are allowed")
            if self.no_of_participants < self.roomslot.room.min_capacity:
                raise Exception(f"Minimum {self.roomslot.room.min_capacity} participants are allowed")
            if Booking.objects.filter(date = self.date,booker = self.booker,roomslot__room = self.roomslot.room,status = "Approved").exists():
                raise Exception(f"You have already booked {self.roomslot.room} for {self.roomslot.slot} slot today")
            if Booking.objects.filter(date = self.date,roomslot = self.roomslot,status = "Approved").exists():
                raise Exception(f"{self.roomslot.room} has already been booked for the slot {self.roomslot.slot} on date {self.date}")
            print(set(self.requirements),set(self.roomslot.room.available_facilities.values_list('name',flat=True).distinct()))
            if not (set(self.requirements).issubset(set(self.roomslot.room.available_facilities.values_list('name',flat=True).distinct()))):
                raise Exception("Facilities are not matching room")
        super().save(*args, **kwargs)


