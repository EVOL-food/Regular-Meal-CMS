from django.test import TestCase
from delivery.models import DeliveryVendor, DeliverySchedule
import datetime
from model_bakery import baker


class DeliveryVendorTestCase(TestCase):
    def setUp(self) -> None:
        self.delivery_vendor = baker.make_recipe('delivery.fixtures.delivery_vendor')

    def test_field(self):
        self.assertEqual(self.delivery_vendor.price_one_delivery, 42)


class DeliveryScheduleTestCase(TestCase):
    def setUp(self) -> None:
        self.delivery_schedule = baker.make_recipe('delivery.fixtures.delivery_schedule')

    def test_field(self):
        self.assertEqual(self.delivery_schedule.mode, 2)

    def test_foreign_key(self):
        self.assertIsInstance(self.delivery_schedule.delivery_vendor, DeliveryVendor)

    def test_pre_save_time(self):
        self.assertEqual(self.delivery_schedule.delivery_time_start_weekday,
                         datetime.time(10))
        self.assertEqual(self.delivery_schedule.delivery_time_end_weekday,
                         datetime.time(12))
        self.assertEqual(self.delivery_schedule.delivery_time_start_weekend,
                         datetime.time(13))
        self.assertEqual(self.delivery_schedule.delivery_time_end_weekend,
                         datetime.time(15))
        self.delivery_schedule.mode = 1
        self.delivery_schedule.save()
        self.assertEqual(self.delivery_schedule.delivery_time_start_weekday,
                         self.delivery_schedule.delivery_time_start_weekend,
                         datetime.time(10))
        self.assertEqual(self.delivery_schedule.delivery_time_end_weekday,
                         self.delivery_schedule.delivery_time_end_weekend,
                         datetime.time(12))
