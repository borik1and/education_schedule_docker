from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from course.models import Course
from users.models import User


class LessonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(title='Test Course', description='test description')
        self.user = User.objects.create_user(username='testuser', password='password', is_active=True)
        self.token = AccessToken.for_user(self.user)  # Создаем токен для пользователя

    def test_lesson_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))  # Устанавливаем токен в заголовке запроса
        url = reverse('lesson:create')
        data = {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'video_url': 'youtube.com',
            'course': self.course.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
