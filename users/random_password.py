from config import settings
from users.models import User

from django.core.mail import send_mail


def generate_new_password(user: User):
    new_password = User.objects.make_random_password(length=12)
    user.set_password(new_password)
    user.save()

    send_mail(
        subject='Востановление пароля',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )

