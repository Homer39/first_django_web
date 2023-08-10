from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    avatar = models.ImageField(upload_to='users/avatars', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=55, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100,verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
