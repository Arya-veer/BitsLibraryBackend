from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import *

from django import forms
# Register your models here.
admin.site.register(Slot)
# admin.site.register(RoomSlot)
# admin.site.register(Booking)
#import jsoneditor
from django_json_widget.widgets import JSONEditorWidget
import re


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name','cost_per_minute')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','min_capacity','max_capacity')
    list_filter = ('min_capacity','max_capacity',)
    search_fields = ('name',)
    autocomplete_fields = ('available_facilities',)
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }
    ordering = ('name',)


@admin.register(RoomSlot)
class RoomSlotAdmin(admin.ModelAdmin):
    list_display = ('room','slot')
    list_filter = ('room','slot')
    search_fields = ('room__name','slot__starttime','slot__endtime')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):


    list_display = ('booker','status','date','roomslot','amount')
    list_filter = ('status','date','roomslot__room')
    search_fields = ('booker__name','roomslot__room__name','roomslot__slot__starttime','roomslot__slot__endtime')
    autocomplete_fields = ('booker','roomslot')
    date_hierarchy = 'date'
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }
    ordering = ('-date',)


    def amount(self,obj):
        """Gets difference of start and end time in minutes and multiplies it with cost per minute of each facility from requirements"""
        return obj.get_amount()
