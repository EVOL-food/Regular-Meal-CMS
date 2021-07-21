from model_bakery.recipe import Recipe, foreign_key
from menu.models import Menu, DailyMeal, Dish, Category, Ingredient
from model_bakery.random_gen import gen_string
from django.conf import settings

def get_titles():
    titles = {f"title_{language}": gen_string(max_length=10)
              for language, _ in settings.LANGUAGES}
    return titles

category = Recipe(
    Category,
    **get_titles(),
    description='Test Category',
)

ingredient = Recipe(
    Ingredient,
    **get_titles(),
)

dish = Recipe(
    Dish,
    **get_titles(),
    calories=42,
    meal_of_the_day=1,
)

daily_meal = Recipe(
    DailyMeal,
    **get_titles(),
    dish_1=foreign_key(dish),
)

menu = Recipe(
    Menu,
    **get_titles(),
    price_daily=42,
    slug = 'test-menu',
    category=foreign_key(category),
    day_1=foreign_key(daily_meal),
)
