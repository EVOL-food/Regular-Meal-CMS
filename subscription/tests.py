from django.test import TestCase
from subscription.models import Subscription, Order
from delivery.models import DeliveryVendor, DeliverySchedule
from client.models import Client


class SubscriptionTestCase(TestCase):
    fixtures = ['subscription.json']

    def test_get(self):
        subscription = Subscription.objects.get(pk='1')
        self.assertEqual(subscription.days, 7)
        self.assertEqual(subscription.menu.title, "Тест меню")
        self.assertEqual(subscription.price, '3000.00')
        self.assertIsInstance(subscription.delivery_schedule, DeliverySchedule)


class OrderTestCase(TestCase):
    fixtures = ['subscription.json']

    def setUp(self) -> None:
        self.order = Order.objects.get(pk='1')

    def test_get(self):
        self.assertIsInstance(self.order.profile, Client)
        self.assertIsInstance(self.order.subscription, Subscription)
        self.assertEqual(self.order.data_start, "2021-07-08")
        self.assertEqual(self.order.data_end, "2021-07-08")
        self.assertEqual(self.order.price, "18000.00")
        self.assertTrue(self.order.status, True)
        self.assertEqual(self.order.created_at, "2021-07-08T12:42:34.029Z")
