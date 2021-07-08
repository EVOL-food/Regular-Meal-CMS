from django.contrib import admin
from .models import DeliveryVendor, DeliverySchedule

# Register your models here.
class DeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('delivery_time_start', 'delivery_time_end')

admin.site.register(DeliveryVendor)
admin.site.register(DeliverySchedule)