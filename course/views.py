from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from course.serializers import CourseSerializer
from lesson.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ('update', 'retrieve'):
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)