from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from .models import *
# Register your models here.
admin.site.register(LibraryOverview)
admin.site.register(LibraryCollection)
admin.site.register(LibraryCollectionData)
admin.site.register(LibraryRulesAndRegulation)
admin.site.register(Rule)
admin.site.register(Feedback)
admin.site.register(LibraryCommittee)
admin.site.register(LibraryCommitteeMember)
admin.site.register(LibraryTeam)
admin.site.register(LibraryTeamMember)

@admin.register(TabularRule)
class TabularRuleAdmin(admin.ModelAdmin):
    list_display = ("name","parent")
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }