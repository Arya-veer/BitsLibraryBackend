from django.contrib import admin

# Register your models here.
from .models import *
# admin.site.register(LinkSite)

@admin.register(LinkSite)
class LinkSiteAdmin(admin.ModelAdmin):
    list_display = ("name","url")
    search_fields = ("name","url")
    list_filter = ("link_type",)

