from datetime import time
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeliveryVendor(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(max_length=300, verbose_name=_("Description"))
    price_one_delivery = models.DecimalField(default=0.0, max_digits=12, decimal_places=2,
                                             verbose_name=_('Price for one delivery'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Delivery vendor')
        verbose_name_plural = _('Delivery vendors')

class DeliverySchedule(models.Model):
    CHOICES_FOR_MODE = (
        (0, _('7 (Everyday)')),
        (1, _('5 (Weekdays)')),
    )
    CHOICES_FOR_TIME = tuple((time(hour=hour), f'{hour}:00')
                             for hour in range(10, 21))

    delivery_vendor = models.ForeignKey(DeliveryVendor, on_delete=models.CASCADE, null=True,
                                        verbose_name=_("Delivery vendor"))

    delivery_time_start_weekday = models.TimeField(choices=CHOICES_FOR_TIME, default=10,
                                                   verbose_name=_("Delivery time start on weekday"))
    delivery_time_end_weekday = models.TimeField(choices=CHOICES_FOR_TIME, default=11,
                                                 verbose_name=_("Delivery time end on weekday"))

    delivery_time_start_weekend = models.TimeField(choices=CHOICES_FOR_TIME, default=10, blank=True, null=True,
                                                   verbose_name=_("Delivery time start on weekend"))
    delivery_time_end_weekend = models.TimeField(choices=CHOICES_FOR_TIME, default=11, blank=True, null=True,
                                                 verbose_name=_("Delivery time end on weekend"))

    mode = models.PositiveSmallIntegerField(choices=CHOICES_FOR_MODE, default=0,
                                    verbose_name=_("Days a week"))

    def __str__(self):
        return f"{self.delivery_vendor.title}: " \
               f"from {self.delivery_time_start_weekday.hour} to {self.delivery_time_end_weekday.hour}" f"{self.mode}"

    class Meta:
        verbose_name = _('Delivery schedule')
        verbose_name_plural = _('Delivery schedules')