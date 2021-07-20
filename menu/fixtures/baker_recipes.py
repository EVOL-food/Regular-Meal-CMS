from model_bakery.recipe import Recipe, foreign_key

from menu.models import Menu, DailyMeal, Dish, Category, Ingredient

category = Recipe(
    Category,
    title='Test Category',
    description='Test Category',
)

ingredient = Recipe(
    Ingredient
)

dish = Recipe(
    Dish,
    calories=42,
    meal_of_the_day=1
)

daily_meal = Recipe(
    DailyMeal,
    dish_1=foreign_key(dish),
    dish_2=foreign_key(dish),
    dish_3=foreign_key(dish),
    dish_4=foreign_key(dish),
    dish_5=foreign_key(dish),
)

menu = Recipe(
    Menu,
    title='Test Menu',
    description='Test Menu',
    price_daily=42,
    slug = 'test-menu',
    category=foreign_key(category),
    day_1=foreign_key(daily_meal),
    day_2=foreign_key(daily_meal),
    day_3=foreign_key(daily_meal),
    day_4=foreign_key(daily_meal),
    day_5=foreign_key(daily_meal),
    day_6=foreign_key(daily_meal),
    day_7=foreign_key(daily_meal),
)
