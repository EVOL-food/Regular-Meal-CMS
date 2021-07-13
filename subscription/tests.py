from django.test import TestCase
from subscription.models import Subscription, Order
from delivery.models import DeliveryVendor, DeliverySchedule
from client.models import Client
import datetime


class SubscriptionTestCase(TestCase):
    fixtures = ['subscription.json']

    def setUp(self) -> None:
        self.subscription = Subscription.objects.get(pk='2')

    def test_get(self):
        self.assertEqual(self.subscription.days, 10)
        self.assertEqual(self.subscription.menu.title, 'Тест меню')
        self.assertEqual(self.subscription.price_menu, 6000.00)
        self.assertEqual(self.subscription.price_delivery, 2000.00)
        self.assertEqual(self.subscription.price_total, 8000.00)
        self.assertIsInstance(self.subscription.delivery_schedule, DeliverySchedule)

    def test_pre_save(self):
        self.subscription.price_menu = self.subscription.menu.price_daily * self.subscription.days
        self.subscription.price_delivery = self.subscription.delivery_schedule.delivery_vendor.price_one_delivery * \
                                           self.subscription.days
        self.subscription.price_total = self.subscription.price_menu + self.subscription.price_delivery

        self.subscription.save()

        self.assertEqual(self.subscription.price_menu,
                         self.subscription.menu.price_daily * self.subscription.days)
        self.assertEqual(self.subscription.price_delivery,
                         self.subscription.delivery_schedule.delivery_vendor.price_one_delivery * \
                         self.subscription.days)
        self.assertEqual(self.subscription.price_total,
                         self.subscription.price_menu + self.subscription.price_delivery)

class OrderTestCase(TestCase):
    fixtures = ['subscription.json']

    def setUp(self) -> None:
        self.order = Order.objects.get(pk='2')

    def test_get(self):
        self.assertIsInstance(self.order.profile, Client)
        self.assertIsInstance(self.order.subscription, Subscription)
        self.assertEqual(self.order.data_start, datetime.date(2021, 7, 11))
        self.assertEqual(self.order.data_end.day, datetime.date(2021, 7, 21).day)
        self.assertEqual(self.order.price, 8000.00)
        self.assertTrue(self.order.status, True)
        self.assertEqual(self.order.created_at.day, datetime.date(2021, 7, 11).day)

    def test_pre_save(self):
        self.order.price = self.order.subscription.price_total
        self.order.data_end = self.order.data_start + datetime.timedelta(days=self.order.subscription.days)

        self.order.save()

        self.assertEqual(self.assertEqual(self.order.price, self.order.subscription.price_total))
        self.assertEqual(self.order.data_end, self.order.data_start + datetime.timedelta(days=self.order.subscription.days))
