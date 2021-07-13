import datetime
from django.test import TestCase
from model_bakery import baker
from subscription.models import Subscription, Order
from delivery.models import DeliverySchedule
from menu.models import Menu
from client.models import Client


class SubscriptionTestCase(TestCase):
    def setUp(self) -> None:
        self.subscription = baker.make_recipe('subscription.fixtures.subscription')

    def test_field(self):
        self.assertEqual(self.subscription.days, 28)
        self.assertEqual(self.subscription.weekdays_only, 0)

    def test_foreign_key(self):
        self.assertIsInstance(self.subscription.menu, Menu)
        self.assertIsInstance(self.subscription.delivery_schedule,
                              DeliverySchedule)
        self.assertEqual(self.subscription.menu.title, 'Test Menu')
        self.assertEqual(self.subscription.delivery_schedule.delivery_vendor.title,
                         'Test Delivery Vendor')

    def test_pre_save(self):
        self.assertEqual(self.subscription.price_menu,
                         self.subscription.menu.price_daily * self.subscription.days)
        self.assertEqual(self.subscription.price_delivery,
                         self.subscription.delivery_schedule.delivery_vendor.price_one_delivery
                         * self.subscription.days)
        self.assertEqual(self.subscription.price_total,
                         self.subscription.price_delivery + self.subscription.price_menu)
        self.subscription.weekdays_only = True
        self.subscription.save()
        days = round(self.subscription.days / 7) * 5
        self.assertEqual(self.subscription.price_menu,
                         self.subscription.menu.price_daily * days)
        self.assertEqual(self.subscription.price_delivery,
                         self.subscription.delivery_schedule.delivery_vendor.price_one_delivery
                         * days)
        self.assertEqual(self.subscription.price_total,
                         self.subscription.price_delivery + self.subscription.price_menu)


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        self.order = baker.make_recipe('subscription.fixtures.order')

    def test_get(self):
        self.assertIsInstance(self.order.profile, Client)
        self.assertIsInstance(self.order.subscription, Subscription)
        self.assertEqual(self.order.data_start, datetime.date(2021, 7, 11))
        self.assertTrue(self.order.status, True)
        self.assertEqual(self.order.created_at.day, datetime.date(2021, 7, 11).day)

    def test_pre_save(self):
        self.assertEqual(self.order.price, 8000.00)
        self.assertEqual(self.order.data_end.day, datetime.date(2021, 7, 21).day)
