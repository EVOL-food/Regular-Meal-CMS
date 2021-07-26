from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule
from django.utils.translation import gettext_lazy as _
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
    inlines = (DeliveryScheduleInlineAdmin,)
    fieldsets = (
        (_('General'), {
            'fields': ('title', 'price_one_delivery', 'description', 'id'),
            'classes': ('baton-tabs-init', 'baton-tab-group-delivery--inline-deliveryschedule',)
        }),
    )
    tab_classes = fieldsets[0][1]["classes"]

    readonly_fields = ('id',)

    list_display = (
        'title',
        'description',
        'price_one_delivery',
        'id'
    )
    list_filter = (('price_one_delivery', SliderNumericFilter),)

    def get_inline_instances(self, request, obj=None):
        inlines = super(DeliveryVendorAdmin, self).get_inline_instances(request, obj=None)
        if not obj:
            return tuple()
        else:
            return inlines

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DeliveryVendorAdmin, self).get_fieldsets(request, obj=None)
        if not obj:
            new_classes = tuple(class_ for class_ in self.tab_classes
                                if "inline" not in class_)
            fieldsets[0][1]["classes"] = new_classes
        else:
            fieldsets[0][1]["classes"] = self.tab_classes
        return fieldsets


class DeliveryScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('delivery_vendor', 'everyday_same_time')
        }),
        (_('Delivery time'), {
            'fields': ('delivery_time_start_weekday',
                       'delivery_time_end_weekday',
                       'delivery_time_start_weekend',
                       'delivery_time_end_weekend',)
        }),
        (None, {
            'fields': ('id',)
        }),
    )
    list_filter = (
        'everyday_same_time',
        'delivery_vendor'
    )
    list_display = ('delivery_vendor',
                    'delivery_time_start_weekday',
                    'delivery_time_end_weekday',
                    'delivery_time_start_weekend',
                    'delivery_time_end_weekend',
                    'everyday_same_time',
                    )
    search_fields = ('delivery_vendor__title', 'delivery_time_start_weekday',
                     'delivery_time_end_weekday', 'delivery_time_start_weekend',
                     'delivery_time_end_weekend')

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.everyday_same_time:
                return ('id', 'delivery_time_start_weekend',
                        'delivery_time_end_weekend')
        except AttributeError:
            return ('id', 'delivery_time_start_weekend',
                    'delivery_time_end_weekend')
        else:
            return tuple()


admin.site.register(DeliveryVendor, DeliveryVendorAdmin)
admin.site.register(DeliverySchedule, DeliveryScheduleAdmin)
