from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from course.models import Course
from lesson.models import Lesson
from users.models import User


class LessonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(title='Test Course', description='test description')
        self.user = User.objects.create_user(username='testuser', password='password', is_active=True)
        self.token = AccessToken.for_user(self.user)  # Создаем токен для пользователя

    def test_lesson_create(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.token))  # Устанавливаем токен в заголовке запроса
        url = reverse('lesson:create')
        data = {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'video_url': 'youtube.com',
            'course': self.course.id
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Lesson')
        self.assertEqual(response.data['description'], 'Test Description')
        self.assertEqual(response.data['video_url'], 'youtube.com')
        self.assertTrue(Lesson.objects.filter(title='Test Lesson').exists())

    def test_lesson_list(self):
        """ Test that we can list all lessons """
        Lesson.objects.create(title='Test Lesson', description='Test Description', video_url='youtube.com',
                              course=self.course)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.token))  # Устанавливаем токен в заголовке запроса
        url = reverse('lesson:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе есть данные
        self.assertTrue(response.data)

        # Проверяем, что в ответе есть ожидаемые данные урока
        lesson_data = response.data['results'][0]  # Получаем первый урок из списка
        self.assertEqual(lesson_data['title'], 'Test Lesson')
        self.assertEqual(lesson_data['description'], 'Test Description')
        self.assertEqual(lesson_data['video_url'], 'youtube.com')
