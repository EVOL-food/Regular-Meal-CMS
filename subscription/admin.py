from django.contrib import admin
from .models import Subscription, Order
from django.utils.translation import gettext_lazy as _
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter


class OrderInlineAdmin(admin.StackedInline):
    model = Order
    fk_name = 'subscription'
    can_delete = False
    show_change_link = True
    max_num = 0
    fieldsets = (
        (None, {
            'fields': tuple()
        }),
    )


class SubscriptionAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    inlines = (OrderInlineAdmin,)
    fieldsets = (
        (_('General'), {
            'fields': ('menu', 'delivery_schedule', 'days', 'weekdays_only'),
            'classes': ('baton-tabs-init', 'baton-tab-fs-price',
                        'baton-tab-inline-order')
        }),
        (_('Price'), {
            'fields': ('price_menu', 'price_delivery', 'price_total'),
            'classes': ('tab-fs-price',)
        }),
    )
    tab_classes = fieldsets[0][1]["classes"]

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

    def get_form(self, request, obj=None, **kwargs):
        form = super(SubscriptionAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['menu'].widget.can_add_related = False
            form.base_fields['menu'].widget.can_change_related = False
        form.base_fields['delivery_schedule'].widget.can_change_related = False
        form.base_fields['delivery_schedule'].widget.can_delete_related = False
        return form

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj=None)
        if not obj or request.GET.get('_popup'):
            return tuple()
        else:
            return inlines

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SubscriptionAdmin, self).get_fieldsets(request, obj=None)
        if not obj:
            new_classes = tuple(class_ for class_ in self.tab_classes
                                if all(["price" not in class_,
                                        "inline" not in class_]))
            fieldsets[0][1]["classes"] = new_classes
            return fieldsets[:-1]
        else:
            fieldsets[0][1]["classes"] = self.tab_classes
            return fieldsets


class OrderAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (_('General'), {
            'fields': ('profile', 'subscription', 'price'),
            'classes': ('baton-tabs-init', 'baton-tab-fs-status',)
        }),
        (_('Status'), {
            'fields': ('status', 'data_start', 'data_end'),
            'classes': ('tab-fs-status',)
        }),
    )
    list_display = ('profile', 'subscription', 'data_start',
                    'data_end', 'price', 'status', 'created_at')
    search_fields = ('profile__first_name', 'profile__last_name',)
    list_filter = ('status', ('price', SliderNumericFilter), 'created_at',
                   'data_end', 'subscription__delivery_schedule__delivery_vendor',)
    readonly_fields = ('price', 'data_end')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('profile', 'subscription',
                    'data_start') + self.readonly_fields
        else:
            return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['profile'].widget.can_add_related = False
            form.base_fields['profile'].widget.can_change_related = False
            form.base_fields['subscription'].widget.can_change_related = False
            form.base_fields['subscription'].widget.can_delete_related = False
        return form


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Order, OrderAdmin)
