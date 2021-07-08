import unidecode
from django.utils.text import slugify
from django.test import TestCase
from menu.models import Menu, DailyMeal, Dish, Category, Ingredient


class IngredientTestCase(TestCase):
    fixtures = ['dish.json']

    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.get(title="Авокадо")

    def test_field_value(self):
        self.assertEqual(self.ingredient.title, "Авокадо")

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.ingredient.title))
        self.assertEqual(self.ingredient.slug, slug)


class DishTestCase(TestCase):
    fixtures = ['dish.json']

    def setUp(self) -> None:
        self.dish = Dish.objects.get(title="Супертост с авокадо")

    def test_field_value(self):
        self.assertEqual(self.dish.title, "Супертост с авокадо")
        self.assertEqual(self.dish.calories, 713)
        self.assertEqual(self.dish.meal_of_the_day, 2)

    def test_pre_save_slug(self):
        slug = slugify(unidecode.unidecode(self.dish.title))
        self.assertEqual(self.dish.slug, slug)

    def test_many_to_many_ingredients(self):
        ingredients = ['Авокадо', 'Вяленые помидоры', 'Лимонный сок', 'Молотый сушеный чеснок',
                       'Ржаной хлеб', 'Перепелиное яйцо', 'Редис', 'Черные кунжутные семечки',
                       'Соль', 'Черный перец', 'Оливковое масло']
        ingredients_example = [str(ingredient) for ingredient in self.dish.ingredients.all()
                               if isinstance(ingredient, Ingredient)]

        self.assertListEqual(sorted(ingredients_example), sorted(ingredients))


class DailyMealTestCase(TestCase):
    fixtures = ['daily_meal.json']

    def setUp(self) -> None:
        self.daily_meal = DailyMeal.objects.filter(title='Разнообразный понедельник').first()

    def test_field_value(self):
        self.assertEqual(self.daily_meal.title, 'Разнообразный понедельник')

    def test_pre_save_calories(self):
        calories = sum([dish.calories for dish in self.daily_meal.get_all_dishes])
        self.assertEqual(self.daily_meal.calories, calories)

    def test_foreign_key_dishes(self):
        dishes = [str(dish) for dish in self.daily_meal.get_all_dishes
                  if isinstance(dish, Dish)]
        dishes_example = ['Гречневый завтрак', 'Печеная камбала с капустой и пореем',
                          'Салат с пряной говядиной и овощами', 'Супертост с авокадо',
                          'Тыквенный суп с имбирем']
        self.assertListEqual(sorted(dishes), dishes_example)


class MenuTestCase(TestCase):
    fixtures = ['menu.json']

    def setUp(self) -> None:
        self.menu = Menu.objects.filter(title="Тест меню").first()

    def test_field(self):
        self.assertEqual(self.menu.title, "Тест меню")
        self.assertIsNotNone(self.menu.category)
        self.assertEqual(self.menu.calories_daily, 0)

    def test_foreign_key_days(self):
        days = [str(day) for day in self.menu.get_all_days
                if isinstance(day, DailyMeal)]
        days_example = ['Вторник', 'Вторник', 'Вторник', 'Понедельник',
                        'Понедельник', 'Понедельник', 'Понедельник']
        self.assertListEqual(sorted(days), days_example)

    def test_slug_pre_save(self):
        slug = slugify(unidecode.unidecode(self.menu.title))
        self.assertEqual(self.menu.slug, slug)

    def test_price_pre_save(self):
        self.assertEqual(self.menu.price_daily, 600)
        if self.menu.price_custom:
            self.assertEqual(self.menu.price_weekly, 3000)
            self.assertEqual(self.menu.price_monthly, 10000)
        self.menu.price_custom = False
        self.menu.save()
        if not self.menu.price_custom:
            self.assertEqual(self.menu.price_weekly, 4200)
            self.assertEqual(self.menu.price_monthly, 18600)
