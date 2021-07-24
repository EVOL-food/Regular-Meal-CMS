# vim: set fileencoding=utf-8 :
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from . import models
from modeltranslation.admin import TranslationAdmin
from menu.translation import (CategoryTranslationOptions, DishTranslationOptions,
                              DailyMealTranslationOptions, MenuTranslationOptions)

from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline
from django.conf import settings
from . import models


class MenuInlineAdmin(TranslationStackedInline):
    classes = ("collapse",)
    fieldsets = (
        (_('General'), {
            'classes': ('collapse',),
            'fields': ('title', 'description', 'category', 'calories_daily',)
        }),
        (_('Price'), {
            'classes': ('collapse',),
            'fields': ('price_daily', 'price_weekly', 'price_monthly', 'price_auto',)
        }),
        (_('Days'), {
            'classes': ('collapse',),
            'fields': ('day_1', "day_2", "day_3", "day_4", "day_5", "day_6", "day_7",)
        }),
        (_('ID'), {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )
    fk_name = "category"
    model = models.Menu
    can_delete = False
    max_num = 0
    readonly_fields = ('calories_daily', 'slug', 'id',
                       'price_weekly', 'price_monthly',
                       'price_auto', "price_daily") + tuple(f'day_{num}' for num in range(1, 8))
    autocomplete_fields = ('photo', 'category')

    search_fields = [f'day_{num}__title' for num in range(1, 8)]

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')
        search_fields.append(f'category__title_{language}')


# Tabs
class CategoryAdmin(TabbedTranslationAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'photo')
        }),
        (_('ID'), {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )
    inlines = (MenuInlineAdmin,)
    list_display = ('title', 'description', 'slug', 'id')
    search_fields = []
    readonly_fields = ('slug', 'id')
    autocomplete_fields = ('photo',)
    exclude_add = ("photo",)

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')
        search_fields.append(f'description_{language}')

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj=None)
        if request.GET.get('_popup'):
            inline_instances = tuple()
        return inline_instances

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        if request.GET.get('_popup'):
            form.base_fields['photo'].widget.can_add_related = False
            form.base_fields['photo'].widget.can_delete_related = False
            form.base_fields['photo'].widget.can_change_related = False
        return form


class IngredientAdmin(TabbedTranslationAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'id')
        }),
    )

    search_fields = []
    readonly_fields = ('id',)

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)


class DishAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'calories',)
        }),
        (_('Detail'), {
            'fields': ('ingredients', 'meal_of_the_day', 'photo')
        }),
        (_('ID'), {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )
    list_display = ('title', 'calories', 'meal_of_the_day', 'id')
    list_filter = (('calories', SliderNumericFilter), 'meal_of_the_day')
    autocomplete_fields = ('photo', 'ingredients')
    search_fields = ['calories']
    readonly_fields = ('slug', 'id')

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')
        search_fields.append(f'description_{language}')

    def get_form(self, request, obj=None, **kwargs):
        form = super(DishAdmin, self).get_form(request, obj, **kwargs)
        for language in tuple(lang[0] for lang in settings.LANGUAGES):
            form.base_fields[f'title_{language}'].widget.attrs['style'] = 'min-width: 45%;'
            form.base_fields[f'description_{language}'].widget.attrs['style'] = 'min-width: 45%; max-height: 100px;'
        if request.GET.get('_popup'):
            for field in ("photo", "ingredients"):
                form.base_fields[field].widget.can_add_related = False
                form.base_fields[field].widget.can_delete_related = False
                form.base_fields[field].widget.can_change_related = False
        return form


class DailyMealAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'calories',)
        }),
        (_('Dishes'), {
            'fields': ('dish_1', "dish_2", "dish_3", "dish_4", "dish_5",)
        }),
        (_('ID'), {
            'classes': ('collapse',),
            'fields': ('id',),
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

    search_fields = [f'dish_{num}__title_{lang}' for num in range(1, 6)
                     for lang in tuple(lang[0] for lang in settings.LANGUAGES)]
    readonly_fields = ('calories', 'id',)
    autocomplete_fields = ("dish_1", "dish_2", "dish_3", "dish_4", "dish_5",)

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')

    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyMealAdmin, self).get_form(request, obj, **kwargs)
        for language in tuple(lang[0] for lang in settings.LANGUAGES):
            form.base_fields[f'title_{language}'].widget.attrs['style'] = 'min-width: 45%;'
        for num in range(1, 6):
            form.base_fields[f'dish_{num}'].widget.can_delete_related = False
            if request.GET.get('_popup'):
                form.base_fields[f'dish_{num}'].widget.can_add_related = False
                form.base_fields[f'dish_{num}'].widget.can_change_related = False
        return form


class MenuAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'calories_daily',)
        }),
        (_('Price'), {
            'fields': ('price_daily', 'price_weekly', 'price_monthly', 'price_auto',)
        }),
        (_('Days'), {
            'fields': ('day_1', "day_2", "day_3", "day_4", "day_5", "day_6", "day_7",)
        }),
        (_('ID'), {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )

    list_display = (
        'title',
        'category',
        'calories_daily',
        'price_daily',
        'price_monthly',
    )
    list_filter = (
        'category',
        ('calories_daily', SliderNumericFilter),
        'price_auto',
        ('price_daily', SliderNumericFilter),
    )
    autocomplete_fields = ('photo', 'category') + tuple(f'day_{num}' for num in range(1, 8))
    search_fields = [f'day_{num}__title_{language}' for num in range(1, 8) for
                     language in tuple(lang[0] for lang in settings.LANGUAGES)]

    for language in tuple(lang[0] for lang in settings.LANGUAGES):
        search_fields.append(f'title_{language}')
        search_fields.append(f'category__title_{language}')

    readonly_fields = ('calories_daily', 'slug', 'id')

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.price_auto:
                return super(MenuAdmin, self).get_readonly_fields(
                    request, obj) + ['price_weekly', 'price_monthly']
        except AttributeError:
            return super(MenuAdmin, self).get_readonly_fields(
                request, obj) + ['price_weekly', 'price_monthly', 'price_auto']
        else:
            return super(MenuAdmin, self).get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)
        for language in tuple(lang[0] for lang in settings.LANGUAGES):
            form.base_fields[f'title_{language}'].widget.attrs['style'] = 'min-width: 45%;'
            form.base_fields[f'description_{language}'].widget.attrs['style'] = 'min-width: 45%; max-height: 100px;'
            form.base_fields[f'category'].widget.can_delete_related = False
        return form


def _register(model, admin_class):
    admin.site.register(model, admin_class)


translator.register(models.Category, CategoryTranslationOptions)
translator.register(models.Dish, DishTranslationOptions)
translator.register(models.DailyMeal, DailyMealTranslationOptions)


_register(models.Ingredient, IngredientAdmin)
_register(models.Category, CategoryAdmin)
_register(models.Dish, DishAdmin)
_register(models.DailyMeal, DailyMealAdmin)
_register(models.Menu, MenuAdmin)
_register(models.Photo, PhotoAdmin)
