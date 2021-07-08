from django.test import TestCase
from delivery.models import DeliveryVendor, DeliverySchedule
import datetime


class DeliveryVendorTestCase(TestCase):
    fixtures = ['delivery_schedule.json']

    def test_get(self):
        delivery_vendor = DeliveryVendor.objects.get(title='Быстрая доставка')
        self.assertEqual(delivery_vendor.title, 'Быстрая доставка')
        self.assertEqual(delivery_vendor.description, "Компания быстрой доставки")
        self.assertEqual(delivery_vendor.price_one_delivery, 200.00)


class DeliveryScheduleTestCase(TestCase):
    fixtures = ['delivery_schedule.json']

    def test_get(self):
        delivery_schedule = DeliverySchedule.objects.get(pk='3')

        self.assertIsInstance(delivery_schedule.delivery_vendor, DeliveryVendor)
        self.assertEqual(delivery_schedule.delivery_time_start_weekday, datetime.time(11, 0))
        self.assertEqual(delivery_schedule.delivery_time_end_weekday, datetime.time(12, 0))
        self.assertEqual(delivery_schedule.delivery_time_start_weekend, datetime.time(11, 0))
        self.assertEqual(delivery_schedule.delivery_time_end_weekend, datetime.time(12, 0))
        self.assertEqual(delivery_schedule.mode, 1)

