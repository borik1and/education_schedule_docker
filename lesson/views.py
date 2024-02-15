from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from lesson.models import Lesson
from lesson.paginators import LessonPaginator
from lesson.permissions import IsModerator, IsOwner
from lesson.serializers import LessonSerializer
from users.models import CourseSubscription


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = LessonPaginator


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class CourseSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        subscription, created = CourseSubscription.objects.get_or_create(user=request.user, course=course)
        if created:
            subscription.subscribed = True
            subscription.save()
            return Response({'detail': 'Subscription to course set successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You are already subscribed to this course.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        subscription = get_object_or_404(CourseSubscription, user=request.user, course=course)
        subscription.delete()
        return Response({'detail': 'Subscription to course removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
