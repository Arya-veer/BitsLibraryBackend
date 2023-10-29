from django.contrib import admin

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