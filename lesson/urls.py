from rest_framework.routers import DefaultRouter
from django.urls import path
from lesson.views import LessonCreateAPIView, LessonViewSet, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = 'lesson'

router = DefaultRouter()
router.register(r'lesson', LessonViewSet, basename='lesson')

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='create'),
    path('', LessonListAPIView.as_view(), name='list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='get'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),

] + router.urls
