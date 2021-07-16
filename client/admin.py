from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from admin_numeric_filter.admin import NumericFilterModelAdmin


class CustomUserAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number',
                    'gender', 'address', 'created_at')
    list_filter = ('gender',)
    search_fields = ('user', 'first_name', 'last_name', 'phone_number',
                     'gender', 'address', 'created_at')


admin.site.register(Profile, CustomUserAdmin)
admin.site.register(User)
