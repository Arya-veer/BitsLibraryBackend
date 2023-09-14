from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import timedelta


class Room(models.Model):
    name = models.CharField("Room Name",max_length=60,blank=True)
    capacity = models.IntegerField("Room Capacity",null=True)
    num_slots = models.PositiveIntegerField(default=9)
    def __str__(self) -> str:
        return self.name
class Slot(models.Model):    
    slots = models.DurationField("",default=timedelta(hours=1))
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='slots')



class Facilities(models.Model):
    name = models.CharField(max_length=60,blank=True)
    rooms = models.ManyToManyField(Room,related_name='facilities')

    def __str__(self):
        return self.name

class Booking(models.Model):

    booker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='booked_rooms')
    status = models.CharField(max_length=40,choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')],default='Pending')
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='booked_rooms')
    description = models.TextField(blank=True)
    slot = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.booker} - {self.status} - {self.room}"
    


