import json
from django.test import TestCase
from menu.models import Menu, Dish, Category, Ingredient


# Дамп данных с поддержкой Юникода:
# python -Xutf8 ./manage.py dumpdata menu > daily_meal.json


class DishTestCase(TestCase):
    fixtures = ['daily_meal.json']

    def test_get(self):
        dish = Dish.objects.get(title="Супертост с авокадо")
        self.assertEqual(dish.title, "Супертост с авокадо")
        self.assertEqual(dish.calories, 713)
        self.assertEqual(dish.meal_of_the_day, 2)
        ingredients = ['Оливковое масло', 'Авокадо', 'Вяленые помидоры', 'Лимонный сок',
                       'Молотый сушеный чеснок', 'Ржаной хлеб', 'Перепелиное яйцо',
                       'Редис', 'Черные кунжутные семечки', 'Соль', 'Черный перец']
        self.assertEqual([str(ingredient) for ingredient in dish.ingredients.all()],
                         ingredients)
