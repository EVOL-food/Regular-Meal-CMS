from django.conf import settings
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from menu.fixtures import model_recipes


class MenuAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = model_recipes.menu.make(_quantity=2)
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.language = settings.MODELTRANSLATION_LANGUAGES[0]
        cls.api_url_list = reverse('menu-list', kwargs={'language': cls.language})
        cls.api_url_detail = reverse('menu-detail', kwargs={'language': cls.language,
                                                            'id': 1})
        cls.api_url_search = reverse('menu-search', kwargs={'language': cls.language})

    def test_get_menu_list(self):
        response = self.client.get(self.api_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.menu))

    def test_get_menu_detail(self):
        response = self.client.get(self.api_url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data.get("title")), 1)

    def test_get_menu_list_by_category(self):
        self.menu[1].category = model_recipes.category.make(id=400)
        self.menu[1].category = model_recipes.category.make(id=400)
        self.menu[1].save()
        response = self.client.get(self.api_url_list,
                                   {"category": "None"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        response = self.client.get(self.api_url_list,
                                   {"category": self.menu[0].category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.api_url_list,
                                   {"category": self.menu[1].category.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_menu_search_results(self):
        response = self.client.get(self.api_url_search,
                                   {'search': self.menu[0].day_1.dish_1.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("title"), self.menu[0].title)
        self.assertEqual(len(response.data), 2)
