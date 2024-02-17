from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from course.models import Course
from users.models import User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(title='Test Course', description='test description')
        self.user = User.objects.create_user(username='testuser', password='password', is_active=True)
        self.token = AccessToken.for_user(self.user)  # Создаем токен для пользователя

    def test_subscribe(self):
        """Test subscribing"""
        # Устанавливаем токен в заголовке запроса
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Отправляем запрос POST на эндпоинт подписки
        response = self.client.post(reverse('user:course-subscribe', kwargs={'course_id': self.course.pk}))

        # Проверяем, что ответ имеет код статуса 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что в базе данных создана запись подписки для данного пользователя и курса
        self.assertTrue(self.user.course_subscriptions.filter(course=self.course, subscribed=True).exists())
