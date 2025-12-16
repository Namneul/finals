from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    real_name = models.CharField(max_length=30, verbose_name="이름")
    location = models.CharField(max_length=100, verbose_name="사는 지역", blank=True)

    def __str__(self):
        return f"{self.real_name} ({self.username})"