from django.db import models
from django.contrib.auth.models import User
from menu.models import Menu
from delivery.models import DeliverySchedule

# Create your models here.


class Subscription(models.Model):
    days = models.PositiveIntegerField(default=0, blank=True)
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_schedule = models.ForeignKey(DeliverySchedule, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
#    profile = models.ForeignKey(Profile, blank=True, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    data_start = models.DateField(auto_now=True)
    data_end = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

