from django.contrib import admin

# Register your models here.
from .models import *

class DatabaseInline(admin.TabularInline):
    model = Database
    extra = 0

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("name","is_main")
    search_fields = ("name",)
    inlines = [DatabaseInline]

@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ("name","campus","link")
    search_fields = ("name",)
    list_filter = ("campus",)
