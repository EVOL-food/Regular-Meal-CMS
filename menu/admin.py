# vim: set fileencoding=utf-8 :
from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from . import models
from modeltranslation.admin import TranslationAdmin
from menu.translation import (CategoryTranslationOptions, DishTranslationOptions,
                              DailyMealTranslationOptions, MenuTranslationOptions)

from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline


class CategoryAdmin(TabbedTranslationAdmin):
    fieldsets = (
        ('General', {
            'fields': ('title', 'description', 'photo')
        }),
        ('Slug and ID', {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )

    list_display = ('title', 'description', 'slug', 'id')
    search_fields = ('title', 'description')
    readonly_fields = ('slug', 'id')
    autocomplete_fields = ('photo',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)


class DailyMealInlineAdmin(TranslationStackedInline):
    model = models.DailyMeal
    can_delete = False
    fk_name = 'dish_1'
    readonly_fields = ('calories',)
    autocomplete_fields = ("dish_1", "dish_2", "dish_3", "dish_4", "dish_5",)
    max_num = 0


class DishAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        ('General', {
            'fields': ('title', 'description')
        }),
        ('Detail', {
            'fields': ('meal_of_the_day', 'calories', 'photo')
        }),
        ('Slug and ID', {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )
    inlines = (DailyMealInlineAdmin,)
    list_display = ('title', 'calories', 'meal_of_the_day', 'id')
    list_filter = (('calories', SliderNumericFilter), 'meal_of_the_day')
    autocomplete_fields = ('photo',)
    search_fields = ('title_en', 'title_ru', 'calories')
    readonly_fields = ('slug', 'id')

    def get_form(self, request, obj=None, **kwargs):
        form = super(DishAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title_en'].widget.attrs['style'] = 'min-width: 45%;'
        form.base_fields['title_ru'].widget.attrs['style'] = 'min-width: 45%;'
        return form


class DailyMealAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        ('General', {
            'fields': ('title', 'calories', 'id')
        }),
        ('Dishes', {
            'fields': ('dish_1', "dish_2", "dish_3", "dish_4", "dish_5",)
        }),
    )
    list_display = (
        'title',
        'calories',
        'id',
    )
    list_filter = (
        ('calories', SliderNumericFilter),
    )

    search_fields = ('title_en', 'title_ru') + tuple(f'dish_{num}__title_{lang}'
                                                     for num in range(1, 6) for lang in ('en', 'ru'))
    readonly_fields = ('calories', 'id',)
    autocomplete_fields = ("dish_1", "dish_2", "dish_3", "dish_4", "dish_5",)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyMealAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title_en'].widget.attrs['style'] = 'min-width: 45%;'
        form.base_fields['title_ru'].widget.attrs['style'] = 'min-width: 45%;'
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
        ('calories_daily', SliderNumericFilter),
        'price_auto',
        ('price_daily', SliderNumericFilter),
    )
    search_fields = ('title', 'category__title') + tuple(f'day_{num}__title' for num in range(1, 8))
    autocomplete_fields = ('photo',) + tuple(f'day_{num}' for num in range(1, 8))
    readonly_fields = ('calories_daily', 'slug')

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.price_auto:
                return ('price_weekly', 'price_monthly',) + self.readonly_fields
        except AttributeError:
            return ('price_auto', 'price_weekly', 'price_monthly',) + self.readonly_fields
        else:
            return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'min-width: 45%;'
        return form


def _register(model, admin_class):
    admin.site.register(model, admin_class)


translator.register(models.Category, CategoryTranslationOptions)
translator.register(models.Dish, DishTranslationOptions)
translator.register(models.DailyMeal, DailyMealTranslationOptions)


_register(models.Category, CategoryAdmin)
_register(models.Dish, DishAdmin)
_register(models.DailyMeal, DailyMealAdmin)
_register(models.Menu, MenuAdmin)
_register(models.Photo, PhotoAdmin)
