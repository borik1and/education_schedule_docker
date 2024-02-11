from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            username="moderator",
            email='moderator@edu.com',
            first_name='moderator',
            last_name='moderator',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role='moderator'
        )

        user.set_password('1975')
        user.save()

        self.stdout.write(self.style.SUCCESS('Модератор успешно создан.'))
