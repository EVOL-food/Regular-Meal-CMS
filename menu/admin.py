from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline
from django.conf import settings
from . import models


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
    fieldsets = (
        ('General', {
            'classes': ('collapse',),
            'fields': ('title', 'calories', 'id')
        }),
        ('Dishes', {
            'classes': ('collapse',),
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
    model = models.DailyMeal
    can_delete = False
    fk_name = 'dish_1'
    readonly_fields = ('calories', 'id')
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
        for language in tuple(lang[0] for lang in settings.LANGUAGES):
            form.base_fields[f'title_{language}'].widget.attrs['style'] = 'min-width: 45%;'
        return form


class MenuInlineAdmin(TranslationStackedInline):
    fieldsets = (
        ('General', {
            'classes': ('collapse',),
            'fields': ('title', 'description', 'category', 'calories_daily',)
        }),
        ('Price', {
            'classes': ('collapse',),
            'fields': ('price_daily', 'price_weekly', 'price_monthly', 'price_auto',)
        }),
        ('Days', {
            'classes': ('collapse',),
            'fields': ('day_1', "day_2", "day_3", "day_4", "day_5", "day_6", "day_7",)
        }),
        ('Slug and ID', {
            'classes': ('collapse',),
            'fields': ('slug', 'id'),
        }),
    )

    model = models.Menu
    can_delete = False
    fk_name = 'day_1'
    max_num = 0
    readonly_fields = ('calories_daily', 'slug', 'id',
                       'price_weekly', 'price_monthly', 'price_auto', "price_daily")
    autocomplete_fields = ('photo', 'category') + tuple(f'day_{num}' for num in range(1, 8))
    search_fields = ('title', 'category__title') + tuple(f'day_{num}__title' for num in range(1, 8))


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
    inlines = (MenuInlineAdmin,)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyMealAdmin, self).get_form(request, obj, **kwargs)
        for language in tuple(lang[0] for lang in settings.LANGUAGES):
            form.base_fields[f'title_{language}'].widget.attrs['style'] = 'min-width: 45%;'
        return form


class MenuAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        ('General', {
            'fields': ('title', 'description', 'category', 'calories_daily',)
        }),
        ('Price', {
            'fields': ('price_daily', 'price_weekly', 'price_monthly', 'price_auto',)
        }),
        ('Days', {
            'fields': ('day_1', "day_2", "day_3", "day_4", "day_5", "day_6", "day_7",)
        }),
        ('Slug and ID', {
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
    search_fields = ('title', 'category__title') + tuple(f'day_{num}__title' for num in range(1, 8))

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
        return form


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Category, CategoryAdmin)
_register(models.Dish, DishAdmin)
_register(models.DailyMeal, DailyMealAdmin)
_register(models.Menu, MenuAdmin)
_register(models.Photo, PhotoAdmin)
