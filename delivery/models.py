from datetime import time
from django.db import models


class DeliveryVendor(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    price_one_delivery = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title


class DeliverySchedule(models.Model):
    CHOICES_FOR_MODE = (
        (1, 'Каждый день в одно время.'),
        (2, 'Рабочие дни, выходные.'),
    )
    CHOICES_FOR_TIME = tuple((time(hour=hour), f'{hour}:00')
                             for hour in range(10, 21))

    delivery_vendor = models.ForeignKey(DeliveryVendor, on_delete=models.CASCADE, null=True)

    delivery_time_start_weekday = models.TimeField(choices=CHOICES_FOR_TIME, default=10)
    delivery_time_end_weekday = models.TimeField(choices=CHOICES_FOR_TIME, default=11)

    delivery_time_start_weekend = models.TimeField(choices=CHOICES_FOR_TIME, default=10,
                                                   blank=True, null=True)
    delivery_time_end_weekend = models.TimeField(choices=CHOICES_FOR_TIME, default=11,
                                                 blank=True, null=True)

    mode = models.SmallIntegerField(choices=CHOICES_FOR_MODE, default=1)

    def __str__(self):
        return f"{self.delivery_vendor.title}: " \
               f"from {self.delivery_time_start_weekday.hour} to {self.delivery_time_end_weekday.hour}"
