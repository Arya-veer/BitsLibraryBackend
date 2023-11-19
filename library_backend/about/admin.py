from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from .models import *

from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.
admin.site.register(LibraryOverview)
admin.site.register(LibraryCollection)
admin.site.register(LibraryCollectionData)
admin.site.register(LibraryRulesAndRegulation)
admin.site.register(Rule)
admin.site.register(LibraryCommittee)
admin.site.register(LibraryCommitteeMember)
# admin.site.register(LibraryTeam)
admin.site.register(LibraryTeamMember)
admin.site.register(LibraryBrochure)
admin.site.register(LibraryWebsiteUserGuide)
admin.site.register(LibraryCalendar)


@admin.register(LibraryTeam)
class LibraryTeamAdmin(admin.ModelAdmin):
    list_display = ("description","is_current")
    search_fields = ("description",)

    def get_actions(self, request):
        #Disable delete
        actions = super(LibraryTeamAdmin, self).get_actions(request)
        print(actions)
        # del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

@admin.register(TabularRule)
class TabularRuleAdmin(admin.ModelAdmin):
    list_display = ("name","parent")
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title","date","time","venue")
    search_fields = ("title","date","time","venue")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title","date")
    search_fields = ("title","date")

class BookMarqueeResource(resources.ModelResource):

    class Meta:
        model = BookMarquee
        fields = ['isbn']
        import_id_fields = ['isbn']
        # export_order = ['isbn','uploaded_on','is_set']
        skip_unchanged = True
        report_skipped = True
        exclude = ("id",)
        skip_html_diff= True
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        BookMarquee.objects.all().update(is_set=False)
        return super().before_import(dataset, using_transactions, dry_run, **kwargs)


@admin.register(BookMarquee)
class BookMarqueeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("isbn","uploaded_on")
    search_fields = ("isbn","uploaded_on")
    list_filter = ("uploaded_on","is_set")
    actions = ["unset_marquee"]
    resource_class = BookMarqueeResource
    # admin action to unset all selected marquee
    @admin.action(description="Unset selected Image")
    def unset_marquee(self,request,queryset):
        queryset.update(is_set=False)