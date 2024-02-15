from rest_framework import serializers
from course.models import Course
from lesson.serializers import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            return instance.subscribers.filter(user=user).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons')
