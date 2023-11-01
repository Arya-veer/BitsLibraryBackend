from django.contrib import admin

from django.contrib.admin.models import LogEntry

# Register your models here.
from .models import *

@admin.register(FreqAskedQuestion)
class FreqAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ("question","answer","is_set")
    list_filter = ("is_set",)
    search_fields = ("question",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name","created_at","show")
    list_filter = ("show",)
    search_fields = ("name","feedback")


@admin.register(LibraryDocument)
class LibraryDocumentAdmin(admin.ModelAdmin):
    list_display = ("name","created_at")
    search_fields = ("name",)

@admin.register(Revalidate)
class RevalidateAdmin(admin.ModelAdmin):
    list_display = ("url","timestamp","done")
    list_filter = ("done","url")
    search_fields = ("url",)
    actions = ['revalidate']

    @admin.action(description="Revalidate selected urls")
    def revalidate(modeladmin, request, queryset):
        for obj in queryset:
            obj.save()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("object_repr","action_flag","user","change_message","content_type","action_time")
    list_filter = ("action_flag","user","content_type","action_time")
    search_fields = ("object_repr","change_message")