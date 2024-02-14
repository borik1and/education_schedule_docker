from rest_framework import serializers
from lesson.models import Lesson
from lesson.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField()

    def validate_video_url(self, value):
        validator = UrlValidator(field='video_url')
        validator(value)
        return value

    class Meta:
        model = Lesson
        fields = ('title', 'description', 'video_url')
