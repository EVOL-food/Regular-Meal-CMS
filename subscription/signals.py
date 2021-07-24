import unidecode
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from subscription.models import Subscription, Order
from datetime import datetime, timedelta


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
