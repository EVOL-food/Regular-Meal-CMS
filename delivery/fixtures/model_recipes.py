from datetime import time
from model_mommy.recipe import Recipe, foreign_key, related
from model_mommy import seq
from delivery.models import DeliverySchedule, DeliveryVendor

delivery_vendor = Recipe(
    DeliveryVendor,
    title=seq("Title "),
    description=seq("Description "),
    price_one_delivery=seq(50)
)

delivery_schedule = Recipe(
    DeliverySchedule,
    delivery_vendor=foreign_key(delivery_vendor),
    everyday_same_time=False,
    delivery_time_start_weekday=time(hour=10),
    delivery_time_end_weekday=time(hour=12),
    delivery_time_start_weekend=time(hour=13),
    delivery_time_end_weekend=time(hour=15)
)