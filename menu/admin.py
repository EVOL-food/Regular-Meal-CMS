from django.contrib import admin
from .models import Menu, DailyMeal, Dish, Ingredient, Category

# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'calories_daily')


class DailyMealAdmin(admin.ModelAdmin):
    list_display = ('title', 'calories')


class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'calories', 'meal_of_the_day')


admin.site.register(Menu, MenuAdmin)
admin.site.register(DailyMeal, DailyMealAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Ingredient)
admin.site.register(Category)
