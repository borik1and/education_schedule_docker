from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def if_user_not_logged_in():
    users = User.objects.all()
    today = datetime.now().date()
    for user_login in users:
        if user_login.last_login:
            last_login_date = user_login.last_login.date()
            thirty_days_ago = today - timedelta(days=30)
            if last_login_date <= thirty_days_ago:
                user_login.is_active = False
                user_login.save()
