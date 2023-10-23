from django.contrib import admin
from .models import UserProfile,Item,Claim
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name","uid","phone_number")
    search_fields = ("name","uid","phone_number")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name","description","is_approved")
    search_fields = ("name",)

    def is_approved(self,obj):
        return obj.claims.filter(is_approved=True).exists()

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("user","item","date","is_approved")
    search_fields = ("user__name","item__name","date")
    list_filter = ("is_approved",)
