import unidecode
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from menu.models import Category, Dish, DailyMeal, Menu


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Dish)
@receiver(pre_save, sender=Menu)
def pre_save_slug(sender, instance, *args, **kwargs):
    for language, _ in settings.LANGUAGES:
        title = getattr(instance, f"title_{language}")
        setattr(instance, f'slug_{language}',
                slugify(unidecode.unidecode(title)))


@receiver(pre_save, sender=DailyMeal)
def pre_save_daily_meal_calories(sender, instance, *args, **kwargs):
    calories = 0
    for dish in instance.get_all_dishes:
        try:
            calories += dish.calories
        except AttributeError:
            pass

    instance.calories = calories


@receiver(pre_save, sender=Menu)
def pre_save_menu_price(sender, instance, *args, **kwargs):
    if instance.price_auto:
        instance.price_weekly = instance.price_daily * 7
        instance.price_monthly = instance.price_weekly * 4

    instance.calories_daily = round(sum(day.calories for day in instance.get_all_days) / 7)
