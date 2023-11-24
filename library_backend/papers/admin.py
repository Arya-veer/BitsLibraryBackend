from django.contrib import admin

# Register your models here.
from .models import Course, Paper,TextBook

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','course_id','campus')
    search_fields = ('name','course_id')
    list_filter = ('campus',)

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('course','semester','year')
    list_filter = ('course__course_id','semester','year',)
    search_fields = ('course__name','course__course_id','semester','year')
    autocomplete_fields = ('course',)
    actions = ['hide_papers']

    @admin.action(description="Hide selected papers")
    def hide_papers(modeladmin, request, queryset):
        queryset.update(hide = True)


@admin.register(TextBook)
class TextBookAdmin(admin.ModelAdmin):
    list_display = ('title','course')
    list_filter = ('course',)
    search_fields = ('title','course__name','course__course_id')
    autocomplete_fields = ('course',)

