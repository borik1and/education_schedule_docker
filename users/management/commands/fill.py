from django.core.management import BaseCommand
from users.models import Payment, User
from datetime import datetime
from course.models import Course

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            {'email': 'ivan@rambler.ru'},
            {'email': 'piter@mail.ru'}
        ]
        for user_data in users:
            user, created = User.objects.get_or_create(email=user_data['email'])
            if created:
                user.set_password('1234')
                user.save()

        pay_list = [
            {'email': 'ivan@rambler.ru', 'payment_date': '2022-01-01', 'amount_pay': 10000,
             'method_pay': 'cash', 'paid_course': 'Python'},
            {'email': 'piter@mail.ru', 'payment_date': '2023-12-01', 'amount_pay': 9000,
             'method_pay': 'transfer_to_account', 'paid_course': 'Java'}
        ]

        for pay_data in pay_list:
            user_email = pay_data.pop('email')
            user = User.objects.get(email=user_email)
            payment_date = datetime.strptime(pay_data.pop('payment_date'), '%Y-%m-%d').date()
            course_name = pay_data.pop('paid_course')
            course, _ = Course.objects.get_or_create(title=course_name)
            Payment.objects.create(user=user, payment_date=payment_date, paid_course=course, **pay_data)
