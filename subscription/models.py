from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from delivery.models import DeliverySchedule
from menu.models import Menu
from client.models import Client
# Create your models here.


class Subscription(models.Model):
    days = models.PositiveIntegerField(blank=True, default=0)
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE, null=True)
    delivery_schedule = models.ForeignKey(DeliverySchedule, on_delete=models.SET_NULL, null=True)
    price_menu = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_delivery = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.menu.title}, {self.days} days, {self.delivery_schedule.delivery_vendor.title}"


class Order(models.Model):
    STATUS = (
        (1, 'New'),
        (2, 'Accepted'),
        (3, 'OnShipping'),
        (4, 'Completed'),
        (5, 'Canceled'),
    )
    profile = models.ForeignKey(Client, blank=True, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    data_start = models.DateField()
    data_end = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.SmallIntegerField(choices=STATUS, default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}, {self.subscription}"


@receiver(pre_save, sender=Subscription)
def pre_save_order(sender, instance, **kwargs):
    instance.price_menu = instance.menu.price_daily * instance.days
    instance.price_delivery = instance.delivery_schedule.delivery_vendor.price_one_delivery * instance.days
    instance.price_total = instance.price_menu + instance.price_delivery


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):
    instance.price = instance.subscription.price_total
    instance.data_end = instance.data_start + timedelta(days=instance.subscription.days)
