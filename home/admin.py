from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from home.models import User


@admin.register(User)
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
        'username', 'last_name', 'first_name', 'last_name_kana',
        'first_name_kana', 'is_staff'
    )

    search_fields = (
        'username', 'first_name', 'last_name',
        'last_name_kana', 'first_name_kana'
    )
