from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter


class DeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('delivery_vendor',
                    'delivery_time_start_weekday',
                    'delivery_time_end_weekday',
                    'delivery_time_start_weekend',
                    'delivery_time_end_weekend',
                    'mode'
                    )
    list_filter = (
        'mode',
        'delivery_vendor'
    )

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


class DeliveryVendorAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    class CustomSliderNumericFilter(SliderNumericFilter):
        MAX_DECIMALS = 0
        STEP = 1

    list_display = (
        'title',
        'description',
        'price_one_delivery'
    )

    list_filter = (('price_one_delivery', CustomSliderNumericFilter),)


admin.site.register(DeliveryVendor, DeliveryVendorAdmin)
admin.site.register(DeliverySchedule, DeliveryScheduleAdmin)
