from django.contrib import admin
from .models import Menu, DailyMeal, Dish, Ingredient, Category

# Register your models here.
admin.site.register(Menu)
admin.site.register(DailyMeal)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Category)
