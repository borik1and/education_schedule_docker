from django.conf import settings
from django.db import models

from course.models import Course

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    video_url = models.CharField(max_length=250, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
