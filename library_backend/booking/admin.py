from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Room)
admin.site.register(Slot)
admin.site.register(RoomSlot)
admin.site.register(Facility)
admin.site.register(Booking)