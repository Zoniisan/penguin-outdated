from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from home import models


@admin.register(models.User)
class UserAdmin(AuthUserAdmin):
    """ [Admin] PENGUIN アカウント
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人情報', {'fields': (
            'last_name', 'first_name',
            'last_name_kana', 'first_name_kana', 'email', 'tel'
        )}),
        ('所属', {'fields': (
            'faculty', 'grade'
        )}),
        ('権限', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        ('Shibboleth', {
            'fields': ('shib_eptid', 'shib_affiliation'),
        }),
        ('ログ', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username', 'last_name', 'first_name', 'is_staff',
        'last_login', 'date_joined'
    )

    search_fields = (
        'username', 'first_name', 'last_name',
        'last_name_kana', 'first_name_kana'
    )


@admin.register(models.UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    """ [Admin] PENGUIN アカウント
    """
    fieldsets = (
        (None, {'fields': ('email', 'token', 'create_datetime', 'used')}),
    )

    list_display = (
        'email', 'create_datetime', 'used'
    )

    search_fields = (
        'email',
    )

    readonly_fields = (
        'create_datetime',
    )
