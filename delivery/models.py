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
        (True, _('Everyday at the same time')),
        (False, _('Weekdays and weekends')),
    )
    CHOICES_FOR_TIME = tuple((time(hour=hour), f'{hour}:00')
                             for hour in range(10, 21))

    delivery_vendor = models.ForeignKey(DeliveryVendor, on_delete=models.CASCADE, null=True,
                                        verbose_name=_("Delivery vendor"))

    delivery_time_start_weekday = models.TimeField(choices=CHOICES_FOR_TIME,
                                                   default=time(hour=10),
                                                   verbose_name=_("Delivery time start on weekday"))
    delivery_time_end_weekday = models.TimeField(choices=CHOICES_FOR_TIME,
                                                 default=time(hour=11),
                                                 verbose_name=_("Delivery time end on weekday"))

    delivery_time_start_weekend = models.TimeField(choices=CHOICES_FOR_TIME,
                                                   default=time(hour=10),
                                                   verbose_name=_("Delivery time start on weekend"))
    delivery_time_end_weekend = models.TimeField(choices=CHOICES_FOR_TIME,
                                                 default=time(hour=11),
                                                 verbose_name=_("Delivery time end on weekend"))

    everyday_same_time = models.BooleanField(choices=CHOICES_FOR_MODE, default=False,
                                             verbose_name=_("Mode"))

    def __str__(self):
        title = f"{self.delivery_vendor.title}; "
        title += f"{self.delivery_time_start_weekday.hour}:00-{self.delivery_time_end_weekday.hour}:00"
        if not self.everyday_same_time:
            title += f", {self.delivery_time_start_weekend.hour}:00-{self.delivery_time_end_weekend.hour}:00"
        return title


    class Meta:
        verbose_name = _('Delivery schedule')
        verbose_name_plural = _('Delivery schedules')
