from django.test import TestCase
from model_bakery import baker
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from client.models import Client


class ClientCase(TestCase):
    def setUp(self) -> None:
        user = baker.make_recipe('client.fixtures.user')
        self.client = baker.make_recipe('client.fixtures.client',
                                        user=user)

    def test_field(self):
        self.assertEqual(self.client.first_name, 'Mario')

    def test_one_to_one(self):
        self.assertIsInstance(self.client.user, User)

    def test_phone_number(self):
        self.assertRaises(ValidationError, self.client.full_clean)
        self.client.phone_number = '+380954507777'
        self.client.save()
        try:
            self.client.full_clean()
        except ValidationError:
            self.fail("ValidationError has been raised!")



