from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from .models import *
# Register your models here.
admin.site.register(LibraryOverview)
admin.site.register(LibraryCollection)
admin.site.register(LibraryCollectionData)
admin.site.register(LibraryRulesAndRegulation)
admin.site.register(Rule)
admin.site.register(LibraryCommittee)
admin.site.register(LibraryCommitteeMember)
admin.site.register(LibraryTeam)
admin.site.register(LibraryTeamMember)
admin.site.register(LibraryBrochure)
admin.site.register(LibraryTiming)

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