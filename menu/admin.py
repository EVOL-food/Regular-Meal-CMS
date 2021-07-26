from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationStackedInline
from django.conf import settings
from . import models


class FormMixin:
    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj=None)
        if not obj or request.GET.get('_popup'):
            return tuple()
        else:
            return inlines

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=None)
        if not obj:
            new_classes = tuple(class_ for class_ in self.tab_classes
                                if all(["id" not in class_,
                                        "inline" not in class_]))
            fieldsets[0][1]["classes"] = new_classes
            return fieldsets[:-1]
        elif request.GET.get('_popup'):
            new_classes = tuple(class_ for class_ in self.tab_classes
                                if "inline" not in class_)
            fieldsets[0][1]["classes"] = new_classes
            return fieldsets
        else:
            fieldsets[0][1]["classes"] = self.tab_classes
            return fieldsets

    @staticmethod
    def remove_form_permissions(form, fields, perm):
        for field in fields:
            permissions = perm[field]
            try:
                if 'add' in permissions:
                    form.base_fields[field].widget.can_add_related = False
                if 'change' in permissions:
                    form.base_fields[field].widget.can_change_related = False
                if 'delete' in permissions:
                    form.base_fields[field].widget.can_delete_related = False
            except ValueError:
                pass

    @staticmethod
    def change_field_size(form, field, min_width=None, max_height=None,
                          languages=False):
        if not languages:
            fields = [field]
        else:
            fields = [f'{field}_{language}' for language
                      in settings.MODELTRANSLATION_LANGUAGES]
        style = ''
        for field in fields:
            try:
                form_field = form.base_fields[field]
                if min_width:
                    style += f'min-width: {min_width};'
                if max_height:
                    style += f'max-height: {max_height};'
                form_field.widget.attrs['style'] = style
            except ValueError:
                pass


class DishesIngredientsInlineAdmin(admin.StackedInline):
    class Media:
        css = {
            'all': (
                'modeltranslation/css/tabbed_translation_fields.css',
                'admin/css/ingredient.css',
            )
        }

    classes = ('collapse',)
    model = models.IngredientDishesProxy
    extra = 0
    can_delete = False
    max_num = 0
    verbose_name = _("Dish")
    verbose_name_plural = _("Dishes")
    fields = ['dish']

    readonly_fields = ('dish',)


class DailyMealInlineAdmin(TranslationStackedInline, admin.StackedInline):
    model = models.DailyMeal
    can_delete = False
    show_change_link = True
    max_num = 0
    fieldsets = (
        (None, {
            'fields': tuple()
        }),
    )


class DailyMealDish1InlineAdmin(DailyMealInlineAdmin):
    fk_name = 'dish_1'
    verbose_name = _("Breakfast")


class DailyMealDish2InlineAdmin(DailyMealInlineAdmin):
    fk_name = 'dish_2'
    verbose_name = _("Brunch")


class DailyMealDish3InlineAdmin(DailyMealInlineAdmin):
    fk_name = 'dish_3'
    verbose_name = _("Lunch")


class DailyMealDish4InlineAdmin(DailyMealInlineAdmin):
    fk_name = 'dish_4'
    verbose_name = _("Dinner")


class DailyMealDish5InlineAdmin(DailyMealInlineAdmin):
    fk_name = 'dish_5'
    verbose_name = _("Supper")


class MenuInlineAdmin(TranslationStackedInline, admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': tuple()
        }),
    )
    fk_name = "category"
    model = models.Menu
    can_delete = False
    show_change_link = True
    max_num = 0


class MenuDay1InlineAdmin(MenuInlineAdmin):
    fk_name = 'day_1'
    verbose_name = _("Monday")


class MenuDay2InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_2'
    verbose_name = _("Tuesday")


class MenuDay3InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_3'
    verbose_name = _("Wednesday")


class MenuDay4InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_4'


class MenuDay5InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_5'


class MenuDay6InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_6'


class MenuDay7InlineAdmin(MenuDay1InlineAdmin):
    fk_name = 'day_7'


# Tabs
class CategoryAdmin(FormMixin, TabbedTranslationAdmin):
    inlines = (MenuInlineAdmin,)
    list_display = ('title', 'description', 'slug', 'id')
    fieldsets = [
        (_('General'), {
            'fields': ('title', 'description', 'photo'),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-id',
                        'baton-tab-group-menu--inline-menu',)
        }),
        (_('ID'), {
            'fields': ('slug', 'id'),
            'classes': ('tab-fs-id',),
        }),
    ]
    tab_classes = fieldsets[0][1]["classes"]

    readonly_fields = ('slug', 'id')

    autocomplete_fields = ('photo',)

    search_fields = [f'{field}_{lang}'
                     for field in ('title', 'description')
                     for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        self.remove_form_permissions(form, ['photo'], {'photo': ['delete']})
        if request.GET.get('_popup'):
            self.remove_form_permissions(form, ["photo"],
                                         {'photo': ['add', 'change']})
        return form


class IngredientAdmin(TabbedTranslationAdmin, admin.ModelAdmin):
    inlines = (DishesIngredientsInlineAdmin,)
    list_display = ('title', 'id')
    readonly_fields = ('id',)

    search_fields = [f'title_{lang}'
                     for lang in settings.MODELTRANSLATION_LANGUAGES]

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj=None)
        if not obj or request.GET.get('_popup'):
            return tuple()
        else:
            return inlines


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')

    search_fields = ('title',)


class DishAdmin(FormMixin, NumericFilterModelAdmin, TabbedTranslationAdmin):
    class Media:
        css = {
            'all': (
                'modeltranslation/css/tabbed_translation_fields.css',
                'admin/css/dish.css',
            )
        }

    list_display = ('title', 'calories', 'meal_of_the_day', 'id')
    list_filter = (
        ('calories', SliderNumericFilter),
        'meal_of_the_day'
    )

    inlines = (DailyMealDish1InlineAdmin, DailyMealDish2InlineAdmin,
               DailyMealDish3InlineAdmin, DailyMealDish4InlineAdmin, DailyMealDish5InlineAdmin)
    inline_tab = 'baton-tab-group-menu' + ''.join(
        [f"--inline-{day}" for day in ('breakfast', 'brunch', 'lunch',
                                       'dinner', 'supper')]
    )

    fieldsets = [
        (_('General'), {
            'fields': ('title', 'description', 'calories', 'photo'),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-detail',
                        'baton-tab-fs-id', inline_tab)
        }),
        (_('Detail'), {
            'fields': ('ingredients', 'meal_of_the_day'),
            'classes': ('tab-fs-detail',)
        }),
        (_('ID'), {
            'fields': ('slug', 'id'),
            'classes': ('tab-fs-id',)
        }),
    ]
    tab_classes = fieldsets[0][1]["classes"]

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
    class Media:
        css = {
            'all': (
                'modeltranslation/css/tabbed_translation_fields.css',
                'admin/css/daily_meal.css',
            )
        }

    list_display = ('title', 'calories', 'id',)
    list_filter = (
        ('calories', SliderNumericFilter),
    )

    inlines = (MenuDay1InlineAdmin, MenuDay2InlineAdmin, MenuDay3InlineAdmin)
    inline_tab = 'baton-tab-group-menu' + ''.join(
        [f"--inline-{day}" for day in ('monday', 'tuesday', 'wednesday',
                                       'thursday', 'friday', 'saturday', 'sunday')]
    )

    fieldsets = [
        (_('General'), {
            'fields': ('title', 'calories',),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-dishes',
                        'baton-tab-fs-id',
                        inline_tab)
        }),
        (_('Dishes'), {
            'fields': ('dish_1', "dish_2", "dish_3", "dish_4", "dish_5",),
            'classes': ('tab-fs-dishes',)
        }),
        (_('ID'), {
            'fields': ('id',),
            'classes': ('tab-fs-id',)
        }),
    ]
    tab_classes = fieldsets[0][1]["classes"]

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

    fieldsets = [
        (_('General'), {
            'fields': ('title', 'description', 'category', 'calories_daily',),
            'classes': ('order-0', 'baton-tabs-init', 'baton-tab-fs-price',
                        'baton-tab-fs-days', 'baton-tab-fs-id')
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
    ]
    tab_classes = fieldsets[0][1]["classes"]

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
