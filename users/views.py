from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from lesson.permissions import IsOwner
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from rest_framework.filters import OrderingFilter

from users.services import process_payment


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        return Response("User authenticated successfully", status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'method_pay',)
    ordering_fields = ('payment_date',)
    permission_classes = [IsOwner]

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Получаем данные из сериализатора
            amount = serializer.validated_data.get('amount_pay')
            success_url = serializer.validated_data.get('success_url')
            cancel_url = serializer.validated_data.get('cancel_url')
            product_name = serializer.validated_data.get('product_name')

            # Создаем платеж и получаем данные о платеже
            payment_data = process_payment(amount, success_url, cancel_url, product_name)

            return Response(payment_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
