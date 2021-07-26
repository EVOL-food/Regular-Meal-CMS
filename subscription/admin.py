from django.contrib import admin
from .models import Subscription, Order
from django.utils.translation import gettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter


class SubscriptionAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (_('General'), {
            'fields': ('email', 'password', 'last_login'),
            'classes': ('baton-tabs-init', 'baton-tab-fs-permissions',
                        'baton-tab-inline-profile',)
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('tab-fs-permissions',)
        }),
    )
    list_display = ('menu', 'days', 'weekdays_only', 'delivery_schedule',
                    'price_menu', 'price_delivery', 'price_total')
    list_filter = ('menu', ('price_total', SliderNumericFilter),
                   'delivery_schedule__delivery_vendor',
                   ('menu__calories_daily', SliderNumericFilter),)
    search_fields = ('menu__title', 'menu__description', 'delivery_schedule')
    readonly_fields = ('price_menu', 'price_delivery', 'price_total')
    autocomplete_fields = ('menu', 'delivery_schedule')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('menu', 'days', 'weekdays_only') + self.readonly_fields
        else:
            return self.readonly_fields


class OrderAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('profile', 'subscription', 'data_start',
                    'data_end', 'price', 'status', 'created_at')
    search_fields = ('profile__first_name', 'profile__last_name',)
    list_filter = ('status', ('price', SliderNumericFilter), 'created_at',
                   'data_end', 'subscription__delivery_schedule__delivery_vendor', )
    readonly_fields = ('price',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('profile', 'subscription', 'data_start', 'data_end') + self.readonly_fields
        else:
            return self.readonly_fields


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Order, OrderAdmin)
