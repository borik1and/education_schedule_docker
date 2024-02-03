from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'method_pay',)
    ordering_fields = ('payment_date',)
