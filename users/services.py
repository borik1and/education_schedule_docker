import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


def process_payment(request):
    if request.method == 'POST':
        token = request.POST.get('token')  # Токен, сгенерированный Stripe.js
        amount = request.POST.get('amount')  # Сумма к оплате, в центах

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='Оплата за курс'
            )
            # Платеж успешно обработан
            payment = Payment.objects.create(
                user=request.user,  # Предполагается, что информация о пользователе доступна через аутентификацию
                amount_pay=amount,
                method_pay='card',  # Предполагается, что оплата осуществляется картой

            )
            payment_serializer = PaymentSerializer(payment)
            return JsonResponse({'message': 'Платеж успешно обработан', 'payment': payment_serializer.data})
        except stripe.error.CardError as e:
            # Ошибка при обработке платежа
            return JsonResponse({'error': str(e)}, status=402)
