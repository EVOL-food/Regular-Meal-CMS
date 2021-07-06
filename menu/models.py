import unidecode
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(blank=True, null=True)


class Ingredient(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title


class Dish(models.Model):
    title = models.CharField(max_length=60)
    calories = models.PositiveIntegerField(default=0)
    meal_of_the_day = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)])
    slug = models.SlugField(blank=True, null=True)

    ingredients = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return self.title


class DailyMeal(models.Model):
    title = models.CharField(default="", max_length=100)
    dishes = models.ManyToManyField(Dish, blank=True, related_name='daily_meal')
    calories = models.PositiveIntegerField(default=0)


class Menu(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    calories_daily = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    price_custom = models.BooleanField(default=False)
    price_daily = models.DecimalField(default=0, max_digits=5, decimal_places=4,)
    price_weekly = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    price_monthly = models.DecimalField(default=0, max_digits=5, decimal_places=4)

    day_1 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_1")
    day_2 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_2")
    day_3 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_3")
    day_4 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_4")
    day_5 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_5")
    day_6 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_6")
    day_7 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name="day_7")


@receiver(pre_save, sender=Dish)
def delivery_vendor_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(unidecode.unidecode(instance.title))


@receiver(pre_save, sender=Ingredient)
def delivery_vendor_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(unidecode.unidecode(instance.title))
