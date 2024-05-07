from django.contrib import admin
from .models import UserProfile,Item,Claim,ArticleBookRequest,FreeBook,FreeBookPick,FootageRequest
from import_export.admin import ImportExportModelAdmin
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
# Register your models here.

from django.contrib.auth.admin import GroupAdmin,UserAdmin
from django.contrib.auth.models import User, Group
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class UserProfileResource(resources.ModelResource):

    auth_user = fields.Field(column_name='uid', attribute='auth_user',widget=ForeignKeyWidget(User, 'username'))
    # auth_user = fields.Field(column_name='uid', attribute='auth_user', widget=ForeignKeyWidget(User, 'username'))
    email = fields.Field(column_name='email', attribute='auth_user__email')

    def before_import_row(self, row, row_number=None, **kwargs):
        auth_user = User.objects.create_user(username=row["uid"],password = row['uid'],email=row.pop('email'))
        print(row_number)
        return super().before_import_row(row, row_number=row_number, **kwargs)
    
    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, raise_errors=None, **kwargs):
        # return super().import_row(row, instance_loader, using_transactions, dry_run, raise_errors, **kwargs)
        print(row)
    
    class Meta:
        model = UserProfile
        fields = ("id","name","uid","email","user_type","phone_number","auth_user")
        export_order = ("name","uid","phone_number","email")
        import_id_fields = ("uid",)
        skip_unchanged = True
        report_skipped = True
        exclude = ("id",)
        skip_html_diff= True

    
        



@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("name","uid","phone_number")
    search_fields = ("name","uid","phone_number")
    resource_class = UserProfileResource

    def process_import(self, request, *args, **kwargs):
        # print(request.POST)
        return super().process_import(request, *args, **kwargs)


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

@admin.register(FreeBook)
class FreeBookAdmin(admin.ModelAdmin):
    list_display = ("title","author",)
    search_fields = ("title","author")
    ordering = ("-id",)
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }

@admin.register(FreeBookPick)
class FreeBookPickAdmin(admin.ModelAdmin):
    list_display = ("user","book","date","status")
    search_fields = ("user__name","book__title","date")
    list_filter = ("status","book")
    ordering = ("-id",)
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }
    
class UserSetInline(admin.TabularInline):
    model = User.groups.through
    
class UserGroupAdmin(GroupAdmin):
    inlines = [UserSetInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group,UserGroupAdmin)


@admin.register(FootageRequest)
class FootageRequestAdmin(admin.ModelAdmin):
    list_display = ("student","status")
    list_filter = ("status",)
    search_fields = ("student__name","student__uid")