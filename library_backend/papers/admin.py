from django.contrib import admin

# Register your models here.
from .models import Course, Paper,TextBook


class StateFilter(admin.SimpleListFilter):
    title = 'State'

    parameter_name = 'state'

    def lookups(self, request, model_admin):
        lookup_data = [
            ("Has Papers", "Has Papers"),
            ("Has TextBooks", "Has TextBooks"),
            ("Has Both", "Has Both"),
            ("Has Nothing", "Has Nothing"),
        ]

        return lookup_data

    def queryset(self, request, queryset):
        if self.value() == "Has Papers":
            return queryset.filter(id__in = Paper.objects.all().values_list('course',flat=True))
        elif self.value() == "Has TextBooks":
            return queryset.filter(id__in = TextBook.objects.all().values_list('course',flat=True))
        elif self.value() == "Has Both":
            return queryset.filter(id__in = Paper.objects.all().values_list('course',flat=True)).filter(id__in = TextBook.objects.all().values_list('course',flat=True))
        elif self.value() == "Has Nothing":
            return queryset.exclude(id__in = Paper.objects.all().values_list('course',flat=True)).exclude(id__in = TextBook.objects.all().values_list('course',flat=True))
        else:
            return queryset

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','course_id','campus')
    search_fields = ('name','course_id')
    list_filter = ('campus',StateFilter,)

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

