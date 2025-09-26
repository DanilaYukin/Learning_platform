from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Модель пользователя """
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone_number = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Номер телефона"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Фото"
    )
    country = models.CharField(max_length=50, blank=True, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
