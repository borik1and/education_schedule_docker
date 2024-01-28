from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet

app_name = 'course'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
] + router.urls
