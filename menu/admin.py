# vim: set fileencoding=utf-8 :
from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'id')
    search_fields = ('title', 'description')
    readonly_fields = ('slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    search_fields = ('title', 'id')
    readonly_fields = ('slug',)


class DishAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'calories', 'meal_of_the_day', 'id')
    list_filter = (('calories', SliderNumericFilter), 'meal_of_the_day')
    autocomplete_fields = ('ingredients',)
    search_fields = ('title', 'calories', 'ingredients__title')
    readonly_fields = ('slug',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DishAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'min-width: 45%;'
        return form


class DailyMealAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = (
        'title',
        'dish_1',
        'dish_2',
        'dish_3',
        'dish_4',
        'dish_5',
        'calories',
        'id',
    )
    list_filter = (
        ('calories', SliderNumericFilter),
    )
    autocomplete_fields = ('dish_1', 'dish_2', 'dish_3', 'dish_4', 'dish_5')
    search_fields = ('title',) + tuple(f'dish_{num}__title' for num in range(1, 6))
    readonly_fields = ('calories',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyMealAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'min-width: 45%;'
        return form


class MenuAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'calories_daily',
        'price_daily',
        'price_monthly',
        'id',
    )
    list_filter = (
        'category',
        'price_custom',
        ('calories_daily', SliderNumericFilter),
    )
    search_fields = ('title',) + tuple(f'day_{num}__title' for num in range(1, 8))
    readonly_fields = ('calories_daily', 'slug')

    def get_readonly_fields(self, request, obj=None):
        try:
            if not obj.price_custom:
                return self.readonly_fields + ('price_weekly', 'price_monthly',)
        except AttributeError:
            return self.readonly_fields + ('price_weekly', 'price_monthly',)
        else:
            return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'min-width: 45%;'
        return form


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Category, CategoryAdmin)
_register(models.Ingredient, IngredientAdmin)
_register(models.Dish, DishAdmin)
_register(models.DailyMeal, DailyMealAdmin)
_register(models.Menu, MenuAdmin)
