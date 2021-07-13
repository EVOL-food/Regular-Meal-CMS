from datetime import time
from model_bakery.recipe import Recipe, foreign_key
from delivery.models import DeliverySchedule, DeliveryVendor

delivery_vendor = Recipe(
    DeliveryVendor,
    price_one_delivery=42
)

delivery_schedule = Recipe(
    DeliverySchedule,
    delivery_vendor=foreign_key(delivery_vendor),
    mode=2,
    delivery_time_start_weekday=time(hour=10),
    delivery_time_end_weekday=time(hour=12),
    delivery_time_start_weekend=time(hour=13),
    delivery_time_end_weekend=time(hour=15)
)
