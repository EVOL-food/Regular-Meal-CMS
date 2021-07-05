from django.db import models


class DeliveryVendor(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    price_one_delivery = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)


class DeliverySchedule(models.Model):
    delivery_vendor = models.ForeignKey(DeliveryVendor, on_delete=models.CASCADE, null=True)
    delivery_time = models.DurationField()



