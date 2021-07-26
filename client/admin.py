from django.contrib import admin
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Profile


class ProfileAdmin(admin.StackedInline):
    model = Profile
    list_display = ('user', 'first_name', 'last_name', 'phone_number',
                    'gender', 'address', 'created_at')
    list_filter = ('gender',)
    search_fields = ('user', 'first_name', 'last_name', 'phone_number',
                     'gender', 'address', 'created_at')
    can_delete = False
    extra = 0
    max_num = 0
    min_num = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileAdmin,)
    fields = ('email', 'password', 'is_staff', 'is_superuser',
              'groups', 'user_permissions', 'last_login')
    search_fields = ("profile__last_name", "profile__phone_number", "profile__address")
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'profile__gender', 'profile__created_at')




admin.site.register(User, UserAdmin)
