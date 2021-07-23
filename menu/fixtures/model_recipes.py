from model_mommy.recipe import Recipe, foreign_key, related
from model_mommy import seq
from django.conf import settings
from menu.models import Menu, DailyMeal, Dish, Category, Ingredient, Photo

title_fields = {f'title_{language}': seq(f'TITLE {language}')
                for language in settings.MODELTRANSLATION_LANGUAGES}

description_fields = {f'description_{language}': seq(f'DESC {language}')
                      for language in settings.MODELTRANSLATION_LANGUAGES}

category = Recipe(
    Category,
    **title_fields,
    **description_fields,
)

ingredient = Recipe(
    Ingredient,
    **title_fields
)

dish = Recipe(
    Dish,
    **title_fields,
    **description_fields,
    ingredients=related(ingredient, ingredient, ingredient),
    calories=seq(10),
    meal_of_the_day=seq(1)
)


daily_meal = Recipe(
    DailyMeal,
    **title_fields,
    calories=seq(100),
    dish_1=foreign_key(dish),
    dish_2=foreign_key(dish),
    dish_3=foreign_key(dish),
    dish_4=foreign_key(dish)
)

menu = Recipe(
    Menu,
    **title_fields,
    **description_fields,
    calories_daily=seq(1000),
    price_daily=seq(300),
    price_auto=True,
    category=foreign_key(category),
    day_1=foreign_key(daily_meal),
    day_2=foreign_key(daily_meal),
    day_3=foreign_key(daily_meal),
    day_4=foreign_key(daily_meal),
    day_5=foreign_key(daily_meal),
    day_6=foreign_key(daily_meal),
    day_7=foreign_key(daily_meal),
)
