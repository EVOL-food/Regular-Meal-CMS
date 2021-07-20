import unidecode
from model_bakery import baker
from PIL import Image
from unittest import mock
from django.utils.text import slugify
from django.test import TestCase, RequestFactory
from io import BytesIO
from django.core.files.base import ContentFile
from parler.utils.context import switch_language

from menu.models import Menu, DailyMeal, Dish, Category, Ingredient, Photo
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .views import SearchDetailView


class TestCaseWithPhoto(TestCase):
    @mock.patch.object(Photo.objects, 'create',
                       side_effect=lambda **params: Photo(**params))
    def create_photo(self, mocked_create):
        image = BytesIO()
        Image.new('RGBA', size=(20, 20), color=(155, 0, 0)).save(image, 'png')
        thumb_file = ContentFile(image.getvalue(), name='Test Photo')
        return mocked_create(title='Test Photo', image=thumb_file)


class CategoryTestCase(TestCaseWithPhoto):
    def setUp(self) -> None:
        self.category = baker.make_recipe('menu.fixtures.category')

    def test_field_value(self):
        self.assertEqual(self.category.title, "Test Category")

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.category.title))
        self.assertEqual(self.category.slug, slug)

    def test_photo(self):
        self.category.photo = self.create_photo()
        self.assertIsInstance(self.category.photo, Photo)
        self.assertEqual(self.category.photo.image.width, 20)


class IngredientTestCase(TestCase):
    def setUp(self) -> None:
        self.ingredient = baker.make_recipe('menu.fixtures.ingredient',
                                            title='Test Ingredient')

    def test_field_value(self):
        self.assertEqual(self.ingredient.title, "Test Ingredient")

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.ingredient.title))
        self.assertEqual(self.ingredient.slug, slug)


class DishTestCase(TestCaseWithPhoto):
    def setUp(self) -> None:
        ingredients = baker.prepare_recipe('menu.fixtures.ingredient', _quantity=5)
        self.dish = baker.make_recipe('menu.fixtures.dish',
                                      title='Test Dish',
                                      ingredients=ingredients)

    def test_field_value(self):
        self.assertEqual(self.dish.title, "Test Dish")
        self.assertEqual(self.dish.calories, 42)
        self.assertEqual(self.dish.meal_of_the_day, 1)

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.dish.title))
        self.assertEqual(self.dish.slug, slug)

    def test_many_to_many_ingredients(self):
        self.assertEqual(self.dish.ingredients.count(), 5)

    def test_photo(self):
        self.dish.photo = self.create_photo()
        self.assertIsInstance(self.dish.photo, Photo)
        self.assertEqual(self.dish.photo.image.width, 20)


class DailyMealTestCase(TestCase):
    def setUp(self) -> None:
        self.daily_meal = baker.make_recipe('menu.fixtures.daily_meal',
                                            title='Test DailyMeal')

    def test_field_value(self):
        self.assertEqual(self.daily_meal.title, 'Test DailyMeal')

    def test_pre_save_calories(self):
        calories = sum([dish.calories for dish in self.daily_meal.get_all_dishes])
        self.assertEqual(self.daily_meal.calories, calories)

    def test_foreign_key_dishes(self):
        for dish in self.daily_meal.get_all_dishes:
            self.assertIsInstance(dish, Dish)


class MenuTestCase(TestCaseWithPhoto):
    def setUp(self) -> None:
        self.menu = baker.make_recipe('menu.fixtures.menu')

    def test_field(self):
        self.assertEqual(self.menu.title, "Test Menu")
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


class PhotoTestCase(TestCaseWithPhoto):
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
class MenuAPITestCase(APITestCase):
    def setUp(self):
        self.menu = baker.make_recipe('menu.fixtures.menu')
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_get_menu_list_view(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response_filter = self.client.get(reverse('menu-list'), args=self.menu.category.slug)
        self.assertEqual(response_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_filter.data), 1)


    def test_search_detail_view(self):
        request = self.factory.get('/menu/', {'search': 'test-menu'})
        response = SearchDetailView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_get_test_menu_retrieve_detail_view(self):
        response = self.client.get(reverse('menu-detail', args= [self.menu.slug]))
        response_not_found_404 = self.client.get(reverse('menu-detail', args= ['bodi-meniu']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 12)
        self.assertEqual(response_not_found_404.status_code, status.HTTP_404_NOT_FOUND)


