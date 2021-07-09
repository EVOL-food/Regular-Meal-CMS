from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
# Create your models here.

class Client(models.Model):
    GENDER_CHOICES = (
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина'),
        ('Иначе', 'Иначе'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
