from django.contrib import admin

# Register your models here.
from .models import Course, Paper

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','course_id')

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('course','exam','year')
    list_filter = ('course','exam','year')
    search_fields = ('course__name','course__course_id','exam','year')