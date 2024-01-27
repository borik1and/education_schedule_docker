from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet

app_name = 'сourse'

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [

              ] + router.urls
