from django.contrib import admin
from .models import Subscription, Order
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter

class SubscriptionAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('menu', 'days', 'delivery_schedule',
                    'price_menu', 'price_delivery', 'price_total')
    list_filter = ('menu', 'delivery_schedule')
    search_fields = ('menu', 'delivery_schedule')

class OrderAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('profile', 'subscription', 'data_start',
                    'data_end', 'price', 'status', 'created_at')
    search_fields = ('profile', 'subscription', 'status', 'created_at')
    list_filter = ('profile', 'subscription', 'status')

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Order, OrderAdmin)