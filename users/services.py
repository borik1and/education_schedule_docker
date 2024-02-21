import stripe
from django.conf import settings
from .models import Payment
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name):
    product = stripe.Product.create(
        name=name,
        active=True
    )
    return product.id


def create_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # цены в Stripe указываются в копейках
        currency='usd',
    )
    return price.id


def create_checkout_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.id


def process_payment(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        amount = int(request.POST.get('amount'))
        success_url = request.POST.get('success_url')
        cancel_url = request.POST.get('cancel_url')
        product_name = request.POST.get('product_name')

        try:
            # Создаем продукт и цену в Stripe
            product_id = create_product(product_name)
            price_id = create_price(product_id, amount)

            # Создаем сессию для платежа в Stripe
            session_id = create_checkout_session(price_id, success_url, cancel_url)

            # Сохраняем ссылку на оплату в нашей системе
            payment = Payment.objects.create(
                amount_pay=amount,
                product_name=product_name,
                payment_session_id=session_id
            )

            # Возвращаем ответ с данными о платеже
            return JsonResponse({'payment_session_id': session_id, 'payment_id': payment.id})
        except stripe.error.StripeError as e:
            # Обработка ошибок Stripe
            return JsonResponse({'error': str(e)}, status=402)
