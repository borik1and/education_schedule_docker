from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from course.models import Course
from lesson.models import Lesson
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderators')


class User(AbstractUser):
    username = models.CharField(max_length=50, verbose_name='Имя', unique=True, **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Почта', **NULLABLE)

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default='member', verbose_name='Роль')

    def __str__(self):
        return f'{self.username}{self.role}'


class Payment(models.Model):
    PAYMENT_METHODS = (
        ("cash", 'Наличные'),
        ("transfer_to_account", 'перевод на счёт')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    amount_pay = models.IntegerField(verbose_name='сумма оплаты')
    method_pay = models.CharField(max_length=100, choices=PAYMENT_METHODS, verbose_name='способ оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='оплаченный урок', **NULLABLE)
    payment_url = models.URLField(verbose_name='ссылка на оплату', blank=True, null=True)


    def __str__(self):
        return f'{self.user}{self.payment_date}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'оплаты'


class CourseSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_subscriptions',
                             verbose_name='пользователь')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='subscribers',
                               verbose_name='курс')
    subscribed = models.BooleanField(default=False, verbose_name='подписался')

    class Meta:
        unique_together = ['user', 'course']
