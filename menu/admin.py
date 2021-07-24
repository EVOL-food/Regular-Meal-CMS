from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline
from django.conf import settings
from . import models


class FormMixin:
    @staticmethod
    def remove_form_permissions(form, fields, perm):
        for field in fields:
            permissions = perm[field]
            if 'add' in permissions:
                form.base_fields[field].widget.can_add_related = False
            if 'change' in permissions:
                form.base_fields[field].widget.can_change_related = False
            if 'delete' in permissions:
                form.base_fields[field].widget.can_delete_related = False

    @staticmethod
    def change_field_size(form, field, min_width=None, max_height=None,
                          languages=False):
        languages = settings.MODELTRANSLATION_LANGUAGES if languages else settings.LANGUAGES[0][0]
        style = ''
        for language in languages:
            form_field = form.base_fields[f'{field}_{language}']
            if min_width:
                style += f'min-width: {min_width};'
            if max_height:
                style += f'max-height: {max_height};'
            form_field.widget.attrs['style'] = style


class MenuInlineAdmin(TranslationStackedInline, admin.StackedInline):
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

    autocomplete_fields = ('photo', 'category')

    search_fields = [f'day_{num}__title_{language}' for num in range(1, 8) for
                     language in settings.MODELTRANSLATION_LANGUAGES]
    search_fields += [f'{field}_{lang}'
                      for field in ('title', 'description')
                      for lang in settings.MODELTRANSLATION_LANGUAGES]

    readonly_fields = ['calories_daily', 'slug', 'id',
                       'price_weekly', 'price_monthly',
                       'price_auto', "price_daily"]
    readonly_fields += [f'day_{num}' for num in range(1, 8)]


# Tabs
class CategoryAdmin(FormMixin, TabbedTranslationAdmin):
    inlines = (MenuInlineAdmin,)
    list_display = ('title', 'description', 'slug', 'id')
    fieldsets = (
        (_('General'), {
            'fields': ('title', 'description', 'photo'),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-id',
                        'baton-tab-group-menu--inline-menu',)
        }),
        (_('ID'), {
            'fields': ('slug', 'id'),
            'classes': ('tab-fs-id',),
        }),
    )

    readonly_fields = ('slug', 'id')

    autocomplete_fields = ('photo',)

    search_fields = [f'{field}_{lang}'
                     for field in ('title', 'description')
                     for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj=None)
        if request.GET.get('_popup'):
            fieldset_classes = ('order-0', 'baton-tabs-init', 'baton-tab-fs-id',)
            self.fieldsets[0][1]["classes"] = fieldset_classes
            inline_instances = tuple()
        return inline_instances

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        self.remove_form_permissions(form, ['photo'], {'photo': ['delete']})
        if request.GET.get('_popup'):
            self.remove_form_permissions(form, ["photo"],
                                         {'photo': ['add', 'change']})
        return form


class IngredientAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'id')
    fieldsets = (
        (None, {
            'fields': ('title', 'id')
        }),
    )

    readonly_fields = ('id',)

    search_fields = [f'title_{lang}'
                     for lang in settings.MODELTRANSLATION_LANGUAGES]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')

    search_fields = ('title',)


class DishAdmin(FormMixin, NumericFilterModelAdmin, TabbedTranslationAdmin):
    list_display = ('title', 'calories', 'meal_of_the_day', 'id')
    list_filter = (
        ('calories', SliderNumericFilter),
        'meal_of_the_day'
    )

    fieldsets = (
        (_('General'), {
            'fields': ('title', 'description', 'calories', 'photo'),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-detail', 'baton-tab-fs-id',)
        }),
        (_('Detail'), {
            'fields': ('ingredients', 'meal_of_the_day'),
            'classes': ('tab-fs-detail',)
        }),
        (_('ID'), {
            'fields': ('slug', 'id'),
            'classes': ('tab-fs-id',)
        }),
    )

    autocomplete_fields = ('photo', 'ingredients')

    readonly_fields = ('slug', 'id')

    search_fields = ['calories']
    search_fields += [f'{field}_{lang}'
                      for field in ('title', 'description')
                      for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_form(self, request, obj=None, **kwargs):
        form = super(DishAdmin, self).get_form(request, obj, **kwargs)
        self.remove_form_permissions(form, ['photo'], {'photo': ['delete']})
        self.change_field_size(form, 'title',
                               min_width='45%', languages=True)
        self.change_field_size(form, 'description',
                               min_width='45%', max_height='100px', languages=True)
        if request.GET.get('_popup'):
            self.remove_form_permissions(form, ("photo", "ingredients"),
                                         {'photo': ['add', 'change'],
                                          'ingredients': ['add']})
        return form


class DailyMealAdmin(FormMixin, NumericFilterModelAdmin, TabbedTranslationAdmin):
    list_display = ('title', 'calories', 'id',)
    list_filter = (
        ('calories', SliderNumericFilter),
    )

    fieldsets = (
        (_('General'), {
            'fields': ('title', 'calories',),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-dishes', 'baton-tab-fs-id',)
        }),
        (_('Dishes'), {
            'fields': ('dish_1', "dish_2", "dish_3", "dish_4", "dish_5",),
            'classes': ('tab-fs-dishes',)
        }),
        (_('ID'), {
            'fields': ('id',),
            'classes': ('tab-fs-id',)
        }),
    )

    readonly_fields = ('calories', 'id',)

    autocomplete_fields = ("dish_1", "dish_2", "dish_3", "dish_4", "dish_5",)

    search_fields = [f'dish_{num}__title_{lang}'
                     for num in range(1, 6)
                     for lang in settings.MODELTRANSLATION_LANGUAGES]
    search_fields += [f'title_{lang}'
                      for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_form(self, request, obj=None, **kwargs):
        form = super(DailyMealAdmin, self).get_form(request, obj, **kwargs)
        self.change_field_size(form, 'title',
                               min_width='45%', languages=True)
        for num in range(1, 6):
            self.remove_form_permissions(form, [f'dish_{num}'],
                                         {f'dish_{num}': ['delete']})
            if request.GET.get('_popup'):
                self.remove_form_permissions(form, [f'dish_{num}'],
                                             {f'dish_{num}': ['add', 'change']})
        return form


class MenuAdmin(FormMixin, NumericFilterModelAdmin, TabbedTranslationAdmin):
    list_display = ('title', 'category', 'calories_daily', 'price_daily', 'price_monthly',)
    list_filter = (
        'category',
        ('calories_daily', SliderNumericFilter),
        'price_auto',
        ('price_daily', SliderNumericFilter),
    )

    fieldsets = (
        (_('General'), {
            'fields': ('title', 'description', 'category', 'calories_daily',),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-price', 'baton-tab-fs-days', 'baton-tab-fs-id',)
        }),
        (_('Price'), {
            'fields': ('price_daily', 'price_weekly', 'price_monthly', 'price_auto',),
            'classes': ('tab-fs-price',)
        }),
        (_('Days'), {
            'fields': ('day_1', "day_2", "day_3", "day_4", "day_5", "day_6", "day_7",),
            'classes': ('tab-fs-days',)
        }),
        (_('ID'), {
            'fields': ('slug', 'id'),
            'classes': ('tab-fs-id',),
        }),
    )

    readonly_fields = ('calories_daily', 'slug', 'id')

    autocomplete_fields = ['photo', 'category']
    autocomplete_fields += [f'day_{num}' for num in range(1, 8)]

    search_fields = [f'day_{num}__title_{lang}'
                     for num in range(1, 8)
                     for lang in settings.MODELTRANSLATION_LANGUAGES]
    search_fields += [f'{field}_{lang}'
                      for field in ('title', 'description')
                      for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_readonly_fields(self, request, obj=None):
        readonly = super(MenuAdmin, self).get_readonly_fields(request, obj)
        try:
            if obj.price_auto:
                return readonly + ['price_weekly', 'price_monthly']
        except AttributeError:
            return readonly + ['price_weekly', 'price_monthly', 'price_auto']
        else:
            return readonly

    def get_form(self, request, obj=None, **kwargs):
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)
        self.remove_form_permissions(form, ['category'],
                                     {'category': ['delete', 'add']})
        self.change_field_size(form, 'title',
                               min_width='45%', languages=True)
        self.change_field_size(form, 'description',
                               min_width='45%', max_height='100px', languages=True)
        return form


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Ingredient, IngredientAdmin)
_register(models.Category, CategoryAdmin)
_register(models.Dish, DishAdmin)
_register(models.DailyMeal, DailyMealAdmin)
_register(models.Menu, MenuAdmin)
_register(models.Photo, PhotoAdmin)
