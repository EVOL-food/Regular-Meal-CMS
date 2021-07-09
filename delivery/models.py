from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class DeliveryVendor(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    price_one_delivery = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=DeliveryVendor)
def delivery_schedule_pre_save(sender, instance, **kwargs):
    print('DeliverySchedule created.')


class DeliverySchedule(models.Model):
    CHOICES_FOR_MODE = (
        (1, 'Каждый день в одно время.'),
        (2, 'Рабочие дни, выходные.'),
    )

    delivery_vendor = models.ForeignKey(DeliveryVendor, on_delete=models.CASCADE, null=True)

    delivery_time_start_weekday = models.TimeField()
    delivery_time_end_weekday = models.TimeField()

    delivery_time_start_weekend = models.TimeField()
    delivery_time_end_weekend = models.TimeField()

    mode = models.SmallIntegerField(choices=CHOICES_FOR_MODE, default=1)

    def __str__(self):
        return self.delivery_vendor.title

@receiver(pre_save, sender=DeliverySchedule)
def delivery_schedule_pre_save(sender, instance, **kwargs):
    print('DeliverySchedule created.')

