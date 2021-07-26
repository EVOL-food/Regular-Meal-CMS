from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule
from django.utils.translation import ugettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline


# Inlines
class DeliveryScheduleInlineAdmin(admin.StackedInline):
    model = DeliverySchedule
    fk_name = 'delivery_vendor'
    can_delete = False
    show_change_link = True
    max_num = 0
    fieldsets = (
        (None, {
            'fields': tuple()
        }),
    )


# Pages
class DeliveryVendorAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    fieldsets = (
        (_('General'), {
            'fields': ('title',
                       'description',)
        }),
        (_('Price'), {
            'fields': ('price_one_delivery',)
        }),
    )
    list_display = (
        'title',
        'description',
        'price_one_delivery'
    )
    list_filter = (('price_one_delivery', SliderNumericFilter),)


class DeliveryScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('delivery_vendor', 'everyday_same_time',)
        }),
        (_('Delivery time'), {
            'fields': (
                       'delivery_time_start_weekday',
                       'delivery_time_end_weekday',
                       'delivery_time_start_weekend',
                       'delivery_time_end_weekend',)
        }),
    )
    model = DeliverySchedule
    fk_name = 'delivery_vendor'
    list_filter = (
        'everyday_same_time',
        'delivery_vendor'
    )
    list_display = ('delivery_vendor',
                    'delivery_time_start_weekday',
                    'delivery_time_end_weekday',
                    'delivery_time_start_weekend',
                    'delivery_time_end_weekend',
                    'everyday_same_time'
                    )
    search_fields = ('delivery_vendor__title', 'delivery_time_start_weekday',
                     'delivery_time_end_weekday', 'delivery_time_start_weekend',
                     'delivery_time_end_weekend')

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.everyday_same_time:
                return ('delivery_time_start_weekend',
                        'delivery_time_end_weekend')
        except AttributeError:
            return ('delivery_time_start_weekend',
                    'delivery_time_end_weekend')
        else:
            return tuple()


admin.site.register(DeliveryVendor, DeliveryVendorAdmin)
admin.site.register(DeliverySchedule, DeliveryScheduleAdmin)
