from django.db.models.signals import pre_save
from django.dispatch import receiver
from delivery.models import DeliverySchedule


@receiver(pre_save, sender=DeliverySchedule)
def delivery_schedule_pre_save(sender, instance, **kwargs):
    if instance.everyday_same_time:
        instance.delivery_time_start_weekend = instance.delivery_time_start_weekday
        instance.delivery_time_end_weekend = instance.delivery_time_end_weekday
