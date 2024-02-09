from django.contrib import admin
from lesson.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'video_url', 'owner',)
    list_filter = ('owner', 'title',)
