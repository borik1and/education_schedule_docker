from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from course.tasks import check_subscribed
from course.models import Course
from course.serializers import CourseSerializer
from lesson.paginators import LessonPaginator
from lesson.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ('update', 'retrieve'):
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ('destroy',):
            self.permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        check_subscribed.delay(instance.pk)  # Запускаем задачу асинхронно