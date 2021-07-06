from django.test import TestCase
from subscription.models import Subscription, Order


class SubscriptionTestCase(TestCase):
    def setUp(self):
        Subscription.objects.create(days='30', menu="Body", price='6005', delivery_schedule="11.30")

    def test_get(self):
        subscription = Subscription.objects.get(days='30')
        self.assertEqual(subscription.days, '30')


class OrderTestCase(TestCase):
    def setUp(self):
        Order.objects.create(profile='test_profile', subscription='test_subscription', data_start='6.07',
                             data_end='6.08', price='60054', status='True', created_at='06.07')

    def test_get(self):
        order = Order.objects.get(profile='test_profile')
        self.assertEqual(order.profile, 'test_profile')
