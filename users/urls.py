from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)
from users.views import UserViewSet, PaymentViewSet, UserRegistrationView, UserLoginView

app_name = 'user'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'pay', PaymentViewSet, basename='pay')

urlpatterns = [
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('users/register/', UserRegistrationView.as_view(), name='user-registration'),
                  path('users/login/', UserLoginView.as_view(), name='user-login'),
              ] + router.urls
