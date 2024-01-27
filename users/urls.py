from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

app_name = 'user'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [

              ] + router.urls
