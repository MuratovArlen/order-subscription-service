from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
