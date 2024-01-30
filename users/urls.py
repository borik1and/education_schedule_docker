from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentViewSet

app_name = 'user'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'pay', PaymentViewSet, basename='pay')

urlpatterns = [

              ] + router.urls
