from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Room)
admin.site.register(Slot)
# admin.site.register(RoomSlot)
admin.site.register(Facility)
# admin.site.register(Booking)
#import jsoneditor
from django_json_widget.widgets import JSONEditorWidget



@admin.register(RoomSlot)
class RoomSlotAdmin(admin.ModelAdmin):
    list_display = ('room','slot')
    list_filter = ('room','slot')
    search_fields = ('room__name','slot__starttime','slot__endtime')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booker','status','date','roomslot','no_of_participants')
    list_filter = ('status','date')
    search_fields = ('booker__name','roomslot__room__name','roomslot__slot__starttime','roomslot__slot__endtime')
    autocomplete_fields = ('booker','roomslot')
    date_hierarchy = 'date'
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }
    ordering = ('-date',)