from django.contrib import admin

from course.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'owner',)
    list_filter = ('owner', 'title')


