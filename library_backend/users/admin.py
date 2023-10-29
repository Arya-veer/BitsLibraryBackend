from django.contrib import admin
from .models import UserProfile,Item,Claim,ArticleBookRequest

from django_json_widget.widgets import JSONEditorWidget
from django.db import models
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
    list_filter = ("is_approved","item")


@admin.register(ArticleBookRequest)
class ArticleBookRequestAdmin(admin.ModelAdmin):
    list_display = ("user","title","author","type_doc","status")
    search_fields = ("user__name","title","author")
    list_filter = ("status","type_doc")
    ordering = ("-id",)
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }

    def save_model(self, request, obj, form, change):
        if change:
            obj.status = "Pending"
        super().save_model(request, obj, form, change)