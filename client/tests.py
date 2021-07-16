from django.test import TestCase
from model_bakery import baker
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from rest_framework import status

from rest_framework.test import APITestCase, APIClient
from client.models import Profile


class ProfileTestCase(TestCase):
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


# API authentication tests

class RegistrationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.client.login(username='admin', password='admin')
        cls.user_data = {
            "username": "test",
            "password": "18901te",
            "email": "test@test.com"
        }
        cls.profile_data = {
            "first_name": "test",
            "last_name": "test",
            "phone_number": "+380444607809",
            "address": "dfsdfsdfsdfs",
            "gender": 1
        }
        cls.signup_dict = {
            **cls.user_data,
            "profile": cls.profile_data
        }

    def test_post_correct_data(self):
        response = self.client.post('/api/auth/users/', self.signup_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(username=self.user_data.get("username"))
        new_profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username,
                         self.user_data.get("username"))
        self.assertEqual(new_profile.phone_number,
                         self.profile_data.get("phone_number"))

    def test_post_username_already_exists(self):
        response = self.client.post('/api/auth/users/', self.signup_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/auth/users/', self.signup_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

