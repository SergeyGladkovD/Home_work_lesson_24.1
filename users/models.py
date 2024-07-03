from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email Address", max_length=255)
    phone_number = models.CharField(
        max_length=15, verbose_name="Phone Number", **NULLABLE
    )
    city = models.CharField(max_length=50, verbose_name="City", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Avatar", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
