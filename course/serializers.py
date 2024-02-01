from rest_framework import serializers
from course.models import Course
from lesson.serializers import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons')
