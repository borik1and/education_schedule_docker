from rest_framework.routers import DefaultRouter
from django.urls import path
from course.views import CourseViewSet
from lesson.views import CourseSubscriptionView

app_name = 'course'

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('<int:course_id>/course-subscribe/', CourseSubscriptionView.as_view(), name='course-subscribe'),
    path('<int:course_id>/course-unsubscribe/', CourseSubscriptionView.as_view(), name='course-unsubscribe'),
] + router.urls
