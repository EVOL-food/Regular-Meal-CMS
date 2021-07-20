import calendar
import datetime
import unidecode
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _
from imagekit.cachefiles.strategies import LazyObject
from django.utils.translation import get_language, activate


class CustomImageStrategy(object):
    def on_existence_required(self, file):
        file.generate()

    def on_content_required(self, file):
        file.generate()

    def on_source_saved(self, file):
        file.generate()


class Photo(models.Model):
    title = models.CharField(max_length=60, default="")
    image = models.ImageField(upload_to='menu/photos/', null=True, blank=True)
    image_large = ImageSpecField(source='image', processors=[ResizeToFill(512, 512)], format='PNG',
                                 options={'quality': 70}, cachefile_strategy=CustomImageStrategy)
    image_medium = ImageSpecField(source='image', processors=[ResizeToFill(256, 256)], format='PNG',
                                  options={'quality': 70}, cachefile_strategy=CustomImageStrategy)
    image_small = ImageSpecField(source='image', processors=[ResizeToFill(128, 128)], format='PNG',
                                 options={'quality': 70}, cachefile_strategy=CustomImageStrategy)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=30, default="")
    description = models.TextField(max_length=1000, default="")
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True,
                            default="", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Dish(models.Model):
    title = models.CharField(max_length=60, default="")
    description = models.TextField(default="", max_length=1000)
    calories = models.PositiveIntegerField(default=0)
    meal_of_the_day = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)])
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=60, unique=True,
                            default="", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Dishes'


class DailyMeal(models.Model):
    title = models.CharField(default="", max_length=100)
    dish_1 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='breakfast', verbose_name='breakfast')
    dish_2 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='brunch', verbose_name='brunch')
    dish_3 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='lunch', verbose_name='lunch')
    dish_4 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='dinner', verbose_name='dinner')
    dish_5 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='supper', verbose_name='supper')

    calories = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def get_all_dishes(self):
        dishes = [self.dish_1, self.dish_2,
                  self.dish_3, self.dish_4, self.dish_5]
        return dishes


class Menu(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000 ,default="")
    calories_daily = models.PositiveIntegerField(default=0, verbose_name='Calories average')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True, default="", blank=True, null=True)

    price_auto = models.BooleanField(default=True)
    price_daily = models.DecimalField(default=0, max_digits=5,
                                      decimal_places=2, verbose_name='Daily costs')
    price_weekly = models.DecimalField(default=0, max_digits=7,
                                       decimal_places=2, verbose_name='Weekly costs')
    price_monthly = models.DecimalField(default=0, max_digits=10,
                                        decimal_places=2, verbose_name='Monthly costs')

    day_1 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="monday", verbose_name='monday')
    day_2 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="tuesday", verbose_name="tuesday")
    day_3 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="wednesday", verbose_name="wednesday")
    day_4 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="thursday", verbose_name="thursday")
    day_5 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="friday", verbose_name="friday")
    day_6 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="saturday", verbose_name="saturday")
    day_7 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="sunday", verbose_name="sunday")

    def __str__(self):
        return self.title

    @property
    def get_all_days(self):
        days = [self.day_1, self.day_2, self.day_3,
                self.day_4, self.day_5, self.day_6, self.day_7]
        return days


@receiver(pre_save, sender=Category)
def pre_save_ingredient(sender, instance, *args, **kwargs):
    instance.slug_en = slugify(unidecode.unidecode(instance.title_en))
    instance.slug_ru = slugify(unidecode.unidecode(instance.title_ru))


@receiver(pre_save, sender=Dish)
def pre_save_dish(sender, instance, *args, **kwargs):
    instance.slug_en = slugify(unidecode.unidecode(instance.title_en))
    instance.slug_ru = slugify(unidecode.unidecode(instance.title_ru))


@receiver(pre_save, sender=DailyMeal)
def pre_save_daily_meal(sender, instance, *args, **kwargs):
    calories = [instance.dish_1.calories,
                instance.dish_2.calories,
                instance.dish_3.calories,
                instance.dish_4.calories,
                instance.dish_5.calories]
    instance.calories = sum(calories)


@receiver(pre_save, sender=Menu)
def pre_save_dish(sender, instance, *args, **kwargs):
    instance.slug = slugify(unidecode.unidecode(instance.title))
    if instance.price_auto:
        instance.price_weekly = instance.price_daily * 7
        instance.price_monthly = instance.price_weekly * 4

    instance.calories_daily = round(sum(day.calories for day in instance.get_all_days) / 7)
