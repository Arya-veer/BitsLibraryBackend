from django.contrib import admin

from django_json_widget.widgets import JSONEditorWidget

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
    list_filter = ("campus","is_trial")

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ("name","author","publisher","subject")
    search_fields = ("name","author","publisher__name","subject__name")
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }
    autocomplete_fields = ["publisher","subject"]

@admin.register(EJournal)
class EJournalAdmin(admin.ModelAdmin):
    list_display = ("name","publisher","subject")
    search_fields = ("name","publisher__name","subject__name")
    list_filter = ("publisher","subject")
    formfield_overrides = {
            models.JSONField: {'widget': JSONEditorWidget},
        }

@admin.register(ELearning)
class ELearningAdmin(admin.ModelAdmin):
    list_display = ("site_name",)
    search_fields = ("name","link")

@admin.register(OpenAccess)
class OpenAccessAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name","url")  


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name","campus")
    search_fields = ("name",)
    list_filter = ("campus",)

@admin.register(NewArrival)
class NewArrivalAdmin(admin.ModelAdmin):
    list_display = ("month","year","position")
    search_fields = ("month","year")
    list_filter = ("year",)
    list_editable = ("position",)

@admin.register(DonatedBook)
class DonatedBookAdmin(admin.ModelAdmin):
    list_display = ("id","isbn","donor","book_type")
    list_filter = ("donor","book_type")
    search_fields = ("isbn","donor")


