from celery import shared_task
from django.core.mail import send_mail
from config import settings
from course.models import Course
from users.models import User


@shared_task
def check_subscribed(course_id):
    try:
        course = Course.objects.get(pk=course_id)
        subscribers = User.objects.filter(course_subscription__course=course, course_subscription__subscribed=True)
        for user in subscribers:
            send_mail(
                'Материалы курса обновились',
                'Вы подписаны на обновления, зайдите, чтобы проверить',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
    except Course.DoesNotExist:
        pass  # Обрабатываем случай, когда курс не существует
