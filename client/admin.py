from django.contrib import admin
from .models import Client
from admin_numeric_filter.admin import NumericFilterModelAdmin

class ClientAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name', 'phone_number',
                    'gender', 'address', 'created_at')
    list_filter = ('gender',)
    search_fields = ('user','first_name', 'last_name', 'phone_number',
                     'gender', 'address', 'created_at')

admin.site.register(Client, ClientAdmin)
