from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from rest_framework import status

from rest_framework.test import APITestCase, APIClient
from client.fixtures import model_recipes
from client.models import Profile


class ProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = model_recipes.user.make()
        cls.profile = model_recipes.profile.make(user=cls.user)

    def test_field(self):
        self.assertEqual(self.profile.first_name, 'Name1')

    def test_one_to_one(self):
        self.assertIsInstance(self.profile.user, User)

    def test_phone_number(self):
        # Invalid number
        self.assertRaises(ValidationError, self.profile.full_clean)
        # Valid number
        self.profile.phone_number = '+380954507777'
        self.profile.save()
        try:
            self.profile.full_clean()
        except ValidationError:
            self.fail("ValidationError has been raised!")

    def test_signal_post_save(self):
        self.assertIsInstance(self.user.profile, self.profile.__class__)
        self.assertIsInstance(self.profile.user, self.user.__class__)


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
