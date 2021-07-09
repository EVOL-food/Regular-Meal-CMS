from django.db.models.signals import pre_save
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from delivery.models import DeliverySchedule
from menu.models import Menu
# Create your models here.


class Subscription(models.Model):
    days = models.PositiveIntegerField(blank=True, default=0)
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_schedule = models.ForeignKey(DeliverySchedule, on_delete=models.SET_NULL, null=True)


@receiver(pre_save, sender=Subscription)
def pre_save_order(sender, instance, **kwargs):
    print("Subscription created")


class Order(models.Model):
    STATUS = (
        (1, 'New'),
        (2, 'Accepted'),
        (3, 'OnShipping'),
        (4, 'Completed'),
        (5, 'Canceled'),
    )
    profile = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    data_start = models.DateField(auto_now=True)
    data_end = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.SmallIntegerField(choices=STATUS, default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):
    print("Order created")
