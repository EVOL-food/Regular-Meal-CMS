from django.db import models
from django.dispatch import receiver
from django.db.models import signals
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(blank=True, null=True)


class Ingredient(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)


class Dish(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    calories = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    ingredients = models.ManyToManyField(Ingredient)


class Menu(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    calories_daily = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    price_custom = models.BooleanField(default=False)
    price_daily = models.DecimalField(default=0, max_digits=5, decimal_places=4,)
    price_weekly = models.DecimalField(blank=True, null=True)
    price_monthly = models.DecimalField(blank=True, null=True)

    dishes_day_1 = models.ManyToManyField(Dish)
    dishes_day_2 = models.ManyToManyField(Dish)
    dishes_day_3 = models.ManyToManyField(Dish)
    dishes_day_4 = models.ManyToManyField(Dish)
    dishes_day_5 = models.ManyToManyField(Dish)
    dishes_day_6 = models.ManyToManyField(Dish)
    dishes_day_7 = models.ManyToManyField(Dish)
