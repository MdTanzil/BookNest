from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'username',
        'is_staff', 'is_active', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']

    fieldsets = (
        ('Personal', {
            'fields': (
                'first_name', 'last_name', 'phone',
                'profile_picture', 'address', 'city', 'postcode'
            )
        }),
        ('Auth', {
            'fields': ('email', 'username', 'password')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
