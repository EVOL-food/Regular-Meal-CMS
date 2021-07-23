import datetime
from django.test import TestCase
from delivery.models import DeliverySchedule
from menu.models import Menu
from client.models import Profile
from subscription.models import Subscription
from subscription.fixtures import model_recipes


class SubscriptionTestCase(TestCase):
    def setUp(self) -> None:
        self.subscription = model_recipes.subscription.make()

    def test_field(self):
        self.assertEqual(self.subscription.days, 28)
        self.assertEqual(self.subscription.weekdays_only, 0)

    def test_foreign_key(self):
        self.assertIsInstance(self.subscription.menu, Menu)
        self.assertIsInstance(self.subscription.delivery_schedule,
                              DeliverySchedule)
        self.assertEqual(self.subscription.menu.title, 'TITLE en121')
        self.assertEqual(self.subscription.delivery_schedule.delivery_vendor.title,
                         'Title 1')

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
        self.order = model_recipes.order.make()

    def test_field(self):
        self.assertEqual(self.order.data_start, datetime.date(year=2020, month=1, day=1))
        self.assertTrue(self.order.status, 1)

    def test_foreign_key(self):
        self.assertIsInstance(self.order.profile, Profile)
        self.assertIsInstance(self.order.subscription, Subscription)
        self.assertEqual(self.order.profile.first_name, 'Name1')
        self.assertEqual(self.order.subscription.days, 28)

    def test_pre_save(self):
        self.assertEqual(self.order.price, self.order.subscription.price_total)
        self.assertEqual(self.order.data_end,
                         self.order.data_start + datetime.timedelta(days=self.order.subscription.days))
