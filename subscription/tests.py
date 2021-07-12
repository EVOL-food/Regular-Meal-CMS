from django.test import TestCase
from subscription.models import Subscription, Order
from delivery.models import DeliveryVendor, DeliverySchedule
from client.models import Client
import datetime


class SubscriptionTestCase(TestCase):
    fixtures = ['subscription.json']

    def test_get(self):
        subscription = Subscription.objects.get(pk='2')
        self.assertEqual(subscription.days, 10)
        #self.assertEqual(subscription.menu, '<Menu: Тест меню>')
        #self.assertEqual(subscription.delivery_schedule,
        #                <DeliverySchedule: Быстрая доставка: from 11 to 12>)
        self.assertEqual(subscription.price_menu, 6000.00)
        self.assertEqual(subscription.price_delivery, 2000.00)
        self.assertEqual(subscription.price_total, 8000.00)
        self.assertIsInstance(subscription.delivery_schedule, DeliverySchedule)


class OrderTestCase(TestCase):
    fixtures = ['subscription.json']

    def setUp(self) -> None:
        self.order = Order.objects.get(pk='2')

    def test_get(self):
        self.assertIsInstance(self.order.profile, Client)
        self.assertIsInstance(self.order.subscription, Subscription)
        self.assertEqual(self.order.data_start, datetime.date(2021, 7, 11))
        self.assertEqual(self.order.data_end, datetime.date(2021, 7, 21))
        self.assertEqual(self.order.price, 8000.00)
        self.assertTrue(self.order.status, True)
        #self.assertEqual(self.order.created_at,
                         #datetime.datetime(2021, 7, 11, 23, 55, 27, 534000, tzinfo=<UTC>))
