from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminConfig(UserAdmin):
    model = User

    search_fields = ('email', 'first_name', 'dob')
    list_filter = ('email', 'first_name', 'is_active', 'is_superuser')

    ordering = ('-create_date',)
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'mobile_number',
    )

    readonly_fields = ('create_date',)

    fieldsets = (
        (
            None, {
                'fields': (
                    'email', 'first_name',
                    'last_name', 'mobile_number',
                ),
            },
        ),
        (
            'Verifications',
            {
                'fields': (
                    'is_email_verified',
                    'is_mobile_verified',
                ),
            },
        ),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
