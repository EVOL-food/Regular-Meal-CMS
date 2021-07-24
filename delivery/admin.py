from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule
from django.utils.translation import ugettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

# Tabs
class DeliveryVendorTabbedAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
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

class DeliveryScheduleTabbedAdmin(TabbedTranslationAdmin):
    fieldsets = (
        (_('Delivery vendor'), {
            'fields': ('delivery_vendor',)
        }),
        (_('Delivery time'), {
            'fields': ('delivery_time_start_weekday',
                       'delivery_time_end_weekday',
                       'delivery_time_start_weekend',
                       'delivery_time_end_weekend',)
        }),
        (_('Delivery mode status'), {
            'fields': ('mode',)
        }),
    )
    model = DeliverySchedule
    fk_name = 'delivery_vendor'
    list_filter = (
        'mode',
        'delivery_vendor'
    )
    readonly_fields = ('delivery_time_start_weekend', 'delivery_time_end_weekend',)
    list_display = ('delivery_vendor',
                    'delivery_time_start_weekday',
                    'delivery_time_end_weekday',
                    'delivery_time_start_weekend',
                    'delivery_time_end_weekend',
                    'mode'
    )
    search_fields = ('delivery_vendor__title', 'delivery_time_start_weekday',
                     'delivery_time_end_weekday', 'delivery_time_start_weekend',
                     'delivery_time_end_weekend')
    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.mode == 1:
                return self.readonly_fields + ('delivery_time_start_weekend',
                                               'delivery_time_end_weekend')
        except AttributeError:
            return self.readonly_fields + ('delivery_time_start_weekend',
                                           'delivery_time_end_weekend')
        else:
            return self.readonly_fields



admin.site.register(DeliveryVendor, DeliveryVendorTabbedAdmin)
admin.site.register(DeliverySchedule, DeliveryScheduleTabbedAdmin)
