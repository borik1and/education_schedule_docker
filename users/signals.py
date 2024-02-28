from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import User


@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    User.objects.filter(pk=user.pk).update(last_login=timezone.now())
