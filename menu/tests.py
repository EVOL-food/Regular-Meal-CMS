import unidecode
from django.conf import settings
from model_bakery import baker
from PIL import Image
from unittest import mock
from django.utils.text import slugify
from django.test import TestCase
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework.test import APIRequestFactory
from menu.models import DailyMeal, Category, Photo
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from model_mommy import mommy
from model_mommy import seq
from .views import SearchDetailView
from menu.fixtures.model_recipes import (category, ingredient,
                                         dish, daily_meal, menu)


class PhotoMixin:
    @mock.patch.object(Photo.objects, 'create',
                       side_effect=lambda **params: Photo(**params))
    def create_photo(self, mocked_create):
        image = BytesIO()
        Image.new('RGBA', size=(20, 20), color=(155, 0, 0)).save(image, 'png')
        thumb_file = ContentFile(image.getvalue(), name='Test Photo')
        return mocked_create(title='Test Photo', image=thumb_file)


class TranslateMixin:
    title_fields = {f'title_{language}': seq(f'Title {language}')
                    for language in settings.MODELTRANSLATION_LANGUAGES}


class CategoryTestCase(PhotoMixin, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = category.make()

    def test_field_value(self):
        self.assertGreater(len(self.category.title), 0)

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.category.title))
        self.assertEqual(self.category.slug, slug)

    def test_photo(self):
        self.category.photo = self.create_photo()
        self.assertIsInstance(self.category.photo, Photo)
        self.assertEqual(self.category.photo.image.width, 20)
        self.assertGreater(len(self.category.photo.image_large.name), 0)
        self.assertGreater(len(self.category.photo.image_medium.name), 0)
        self.assertGreater(len(self.category.photo.image_small.name), 0)


class IngredientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.ingredient = ingredient.make()

    def test_field_value(self):
        self.assertGreater(len(self.ingredient.title), 0)


class DishTestCase(PhotoMixin, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.dish = dish.make()

    def test_field_value(self):
        self.assertGreater(len(self.dish.title), 0)
        self.assertGreater(self.dish.calories, 0)
        self.assertIn(self.dish.meal_of_the_day, [1, 2, 3, 4, 5])

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.dish.title))
        self.assertEqual(self.dish.slug, slug)

    def test_many_to_many_ingredients(self):
        self.assertEqual(self.dish.ingredients.count(), 3)

    def test_get_ingredients_list(self):
        self.assertEqual(self.dish.get_ingredients_list,
                         [ingredient.title for ingredient
                          in self.dish.ingredients.all()])

    def test_photo(self):
        self.dish.photo = self.create_photo()
        self.assertIsInstance(self.dish.photo, Photo)
        self.assertEqual(self.dish.photo.image.width, 20)


class DailyMealTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.daily_meal = daily_meal.make()

    def test_field_value(self):
        self.assertGreater(len(self.daily_meal.title), 0)
        # The dish_5 field will be empty for the test
        self.assertIsNone(self.daily_meal.dish_5)

    def test_pre_save_calories(self):
        calories = 0
        for dish in self.daily_meal.get_all_dishes:
            try:
                calories += dish.calories
            except AttributeError:
                pass
        self.assertEqual(self.daily_meal.calories, calories)

    def test_foreign_key_dishes(self):
        # The dish_5 field will be empty for the test
        for dish in self.daily_meal.get_all_dishes[:-1]:
            self.assertGreater(len(dish.title), 0)


class MenuTestCase(PhotoMixin, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.menu = menu.make()

    def test_field(self):
        self.assertGreater(len(self.menu.title), 0)
        self.assertIsInstance(self.menu.category, Category)

    def test_foreign_key_days(self):
        for day in self.menu.get_all_days:
            self.assertIsInstance(day, DailyMeal)

    def test_slug_pre_save(self):
        slug = slugify(unidecode.unidecode(self.menu.title))
        self.assertEqual(self.menu.slug, slug)

    def test_price_pre_save(self):
        price_weekly = self.menu.price_daily * len(self.menu.get_all_days)
        self.menu.price_auto = False
        self.menu.price_weekly -= 42
        self.menu.price_monthly -= 42
        self.menu.save()
        self.assertFalse(self.menu.price_auto)
        self.assertEqual(self.menu.price_weekly, price_weekly - 42)
        self.assertEqual(self.menu.price_monthly, price_weekly * 4 - 42)
        self.menu.price_auto = True
        self.menu.save()
        self.assertEqual(self.menu.price_weekly, price_weekly)
        self.assertEqual(self.menu.price_monthly, price_weekly * 4)

    def test_calories_pre_save(self):
        self.assertEqual(self.menu.calories_daily,
                         round(sum(day.calories for day
                                   in self.menu.get_all_days) / 7))

    def test_photo(self):
        self.photo = self.create_photo()
        self.menu.photo = self.photo
        self.assertIsInstance(self.menu.photo, Photo)
        self.assertEqual(self.menu.photo.image.width, 20)


class PhotoTestCase(PhotoMixin, TestCase):
    def setUp(self) -> None:
        self.photo = self.create_photo()

    def test_image(self):
        self.assertEqual(self.photo.image.name, 'Test Photo')
        self.assertEqual(self.photo.image.width, 20)

    def test_thumbnail(self):
        self.assertEqual(Photo.image_large.spec_id, 'menu:photo:image_large')
        self.assertEqual(Photo.image_medium.spec_id, 'menu:photo:image_medium')
        self.assertEqual(Photo.image_small.spec_id, 'menu:photo:image_small')


# API views tests
class MenuAPITestCase(TranslateMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu = menu.make(_quantity=2)
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
        self.menu[1].category = category.make(id=400)
        self.menu[1].category = category.make(id=400)
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
