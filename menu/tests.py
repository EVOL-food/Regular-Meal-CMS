import json
from django.test import TestCase
from menu.models import Menu, DailyMeal, Dish, Category, Ingredient


class DishTestCase(TestCase):
    fixtures = ['dish.json']

    def test_get(self):
        dish = Dish.objects.get(title="Супертост с авокадо")
        self.assertEqual(dish.title, "Супертост с авокадо")
        self.assertEqual(dish.calories, 713)
        self.assertEqual(dish.meal_of_the_day, 2)
        ingredients = ['Авокадо', 'Вяленые помидоры', 'Лимонный сок', 'Молотый сушеный чеснок',
                       'Ржаной хлеб', 'Перепелиное яйцо', 'Редис', 'Черные кунжутные семечки',
                       'Соль', 'Черный перец', 'Оливковое масло']

        self.assertListEqual(sorted([str(ingredient) for ingredient in dish.ingredients.all()]),
                             sorted(ingredients))


class DailyMealTestCase(TestCase):
    fixtures = ['daily_meal.json']

    def test_get(self):
        daily_meal = DailyMeal.objects.filter(title='Разнообразный понедельник').first()
        self.assertEqual(daily_meal.title, 'Разнообразный понедельник')
        self.assertEqual(daily_meal.calories, 3257)

        dishes = [daily_meal.dish_1.title, daily_meal.dish_2.title,
                  daily_meal.dish_3.title, daily_meal.dish_4.title,
                  daily_meal.dish_5.title]
        dishes_example = ['Гречневый завтрак', 'Печеная камбала с капустой и пореем',
                          'Салат с пряной говядиной и овощами', 'Супертост с авокадо',
                          'Тыквенный суп с имбирем']
        self.assertListEqual(sorted(dishes), dishes_example)


class MenuTestCase(TestCase):
    fixtures = ['menu.json']

    def test_get(self):
        menu = Menu.objects.filter(title="Тест меню").first()
        self.assertEqual(menu.title, "Тест меню")
        self.assertIsNone(menu.category)
        self.assertEqual(menu.calories_daily, 0)

        days = [menu.day_1.title, menu.day_2.title, menu.day_3.title,
                menu.day_4.title, menu.day_5.title, menu.day_6.title,
                menu.day_7.title]
        days_example = ['Вторник', 'Вторник', 'Вторник', 'Понедельник',
                        'Понедельник', 'Понедельник', 'Понедельник']

        self.assertListEqual(sorted(days), days_example)
