from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
    tab_classes = fieldsets[0][1]["classes"]

    list_display = ('email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'profile__gender', 'profile__created_at')

    search_fields = ("profile__last_name", "profile__phone_number", "profile__address")

    readonly_fields = ('email', 'last_login', 'password')


admin.site.register(User, UserAdmin)
