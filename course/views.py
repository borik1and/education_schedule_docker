from rest_framework import viewsets
from course.models import Course
from course.serializers import CourseSerializer
from lesson.permissions import IsOwnerOrStaff, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrStaff, IsModerator]
