from django.db import models

NULLABLE = {'blank': True, 'null': True}


# название,
# описание,
# превью (картинка),
# ссылка на видео.

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    video_url = models.URLField(max_length=250, verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'