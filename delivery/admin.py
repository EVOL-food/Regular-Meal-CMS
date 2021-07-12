from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule
from admin_numeric_filter.admin import NumericFilterModelAdmin


class DeliveryScheduleAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
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
     search_fields = ('delivery_vendor',
                     'delivery_time_start_weekday',
                     'delivery_time_end_weekday',
                     'delivery_time_start_weekend',
                     'delivery_time_end_weekend',
                     'mode'
                      )

class DeliveryVendorAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
     list_display = (
          'title',
          'description',
          'price_one_delivery'
     )
     list_filter = (
          'title',
          'price_one_delivery'
     )
     search_fields = ('title',
                      'description',
                      'price_one_delivery')

admin.site.register(DeliveryVendor, DeliveryVendorAdmin)
admin.site.register(DeliverySchedule, DeliveryScheduleAdmin)