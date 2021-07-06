from django.test import TestCase
from delivery.models import DeliveryVendor, DeliverySchedule


class DeliveryVendorTestCase(TestCase):
    def setUp(self):
        DeliveryVendor.objects.create(title='monday', description='address',
                                      price_one_delivery='12.50')
        DeliveryVendor.objects.create(title='tuesday', description='address',
                                      price_one_delivery='15')

    def test_get(self):
        delivery = DeliveryVendor.objects.get(title='monday')
        delivery2 = DeliveryVendor.objects.get(title='tuesday')
        self.assertEqual(delivery.title, 'monday')
        self.assertEqual(delivery2.title, 'tuesday')


class DeliveryScheduleTestCase(TestCase):
    def setUp(self):
        DeliverySchedule.objects.create(delivery_vendor='test_food', delivery_time='11.30')

    def test_get(self):
        delivery_schedule = DeliverySchedule.objects.get(delivery_vendor='test_food')
        self.assertEqual(delivery_schedule.delivery_vendor, 'test_food')
