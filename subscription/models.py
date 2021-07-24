from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from delivery.models import DeliverySchedule
from menu.models import Menu
from client.models import Profile
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Subscription(models.Model):
    CHOISES = ((7, _('Week (7 days)')), (28, _('Month (28 days)')))

    days = models.PositiveSmallIntegerField(choices=CHOISES, default=28, verbose_name= _('Days'))
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, verbose_name= _('Menu'))
    delivery_schedule = models.ForeignKey(DeliverySchedule, on_delete=models.SET_NULL, null=True,
                                          verbose_name= _('Delivery schedule'))
    weekdays_only = models.BooleanField(default=False, verbose_name= _('Weekdays only'))
    price_menu = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                     verbose_name= _('Price menu'))
    price_delivery = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                         verbose_name= _('Price delivery'))
    price_total = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                      verbose_name= _('Price total'))

    def __str__(self):
        return f"{self.menu.title}, {self.days} days, {self.delivery_schedule.delivery_vendor.title}"

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class Order(models.Model):
    STATUS = (
        (1, _('New')),
        (2, _('Accepted')),
        (3, _('OnShipping')),
        (4, _('Completed')),
        (5, _('Canceled')),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                verbose_name= _('Profile'))
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True,
                                     verbose_name= _('Subscription'))
    data_start = models.DateField(verbose_name= _('Data start'))
    data_end = models.DateField(blank=True, null=True, verbose_name= _('Data end'))
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name= _('Price'))
    status = models.SmallIntegerField(choices=STATUS, default=1, verbose_name= _('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= _('Created at'))

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}, {self.subscription}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


@receiver(pre_save, sender=Subscription)
def pre_save_subscription(sender, instance, **kwargs):
    if not instance.weekdays_only:
        instance.price_menu = instance.menu.price_daily * instance.days
        instance.price_delivery = instance.delivery_schedule.delivery_vendor.price_one_delivery * instance.days
        instance.price_total = instance.price_menu + instance.price_delivery
    else:
        days = round(instance.days / 7) * 5
        instance.price_menu = days * instance.menu.price_daily
        instance.price_delivery = instance.delivery_schedule.delivery_vendor.price_one_delivery * days
        instance.price_total = instance.price_menu + instance.price_delivery


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):
    instance.price = instance.subscription.price_total
    instance.data_end = instance.data_start + timedelta(days=instance.subscription.days)
