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
    list_filter = ("publisher","subject")

@admin.register(EJournal)
class EJournalAdmin(admin.ModelAdmin):
    list_display = ("name","publisher","subject")
    search_fields = ("name","publisher__name","subject__name")
    list_filter = ("publisher","subject")

@admin.register(ELearning)
class ELearningAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name","url")

@admin.register(OpenAccess)
class OpenAccessAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name","url")  



