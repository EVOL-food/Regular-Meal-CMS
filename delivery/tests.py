import datetime
from django.test import TestCase
from model_bakery import baker
from delivery.models import DeliveryVendor
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class DeliveryVendorTestCase(TestCase):
    def setUp(self) -> None:
        self.delivery_vendor = baker.make_recipe('delivery.fixtures.delivery_vendor')

    def test_field(self):
        self.assertEqual(self.delivery_vendor.title, 'Test Delivery Vendor')
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

# Api view test
class DeliveryVendorAPITest(TestCase):
    def setUp(self) -> None:
        self.delivery_vendor = baker.make_recipe('delivery.fixtures.delivery_vendor')
        self.client = APIClient()

    def test_get_delivery_vendor_list_view(self):
        response = self.client.get(reverse('delivery-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)