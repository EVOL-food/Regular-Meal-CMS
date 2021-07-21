from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from admin_numeric_filter.admin import NumericFilterModelAdmin


class ProfileAdmin(admin.StackedInline):
    model = Profile
    list_display = ('user', 'first_name', 'last_name', 'phone_number',
                    'gender', 'address', 'created_at')
    list_filter = ('gender',)
    search_fields = ('user', 'first_name', 'last_name', 'phone_number',
                     'gender', 'address', 'created_at')
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'email', 'last_login', 'is_superuser',
              'is_staff', 'groups', 'user_permissions')
    search_fields = ("profile__last_name", "profile__phone_number", "profile__address")
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'profile__gender', 'profile__created_at')
    inlines = (ProfileAdmin,)


admin.site.register(User, UserAdmin)
