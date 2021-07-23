import datetime
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from delivery.fixtures import model_recipes


class DeliveryVendorAPITest(TestCase):
    def setUp(self) -> None:
        self.delivery_vendor = model_recipes.delivery_vendor.make()
        self.client = APIClient()

    def test_get_delivery_vendor_list_view(self):
        response = self.client.get(reverse('delivery-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
