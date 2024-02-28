from datetime import datetime, timedelta
from users.models import User


def if_user_not_logged_in(user_id):
    user_login = User.objects.filter(id=user_id).first()
    if user_login and user_login.last_login:
        today = datetime.now().date()
        last_login_date = user_login.last_login.date()
        thirty_days_ago = today - timedelta(days=30)
        if last_login_date <= thirty_days_ago:
            user_login.is_active = False
            user_login.save()
