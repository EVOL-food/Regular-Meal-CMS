from django.test import TestCase
from menu.models import Menu
from subscription.models import Subscription, Order


class MenuTestCase(TestCase):
    def setUp(self):
        pass

    def test_get(self):
        pass


class SubscriptionTestCase(TestCase):
    def setUp(self):
        Subscription.objects.create(days='30', menu="Body", price='6005', delivery_schedule="11.30")

    def test_get(self):
        subscription = Subscription.objects.get(days='30')
        self.assertEqual(subscription.days, '30')


class OrderTestCase(TestCase):
    def setUp(self):
        pass

    def test_get(self):
        pass