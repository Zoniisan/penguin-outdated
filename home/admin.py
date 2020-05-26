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


@admin.register(models.OfficeGroup)
class OfficeGroupAdmin(admin.ModelAdmin):
    """ [Admin] 部局担当
    """
    fieldsets = (
        ('基本情報', {'fields': ('name', 'email', 'slack_ch')}),
        ('auth.Group との関連', {'fields': ('group',)}),
    )

    list_display = (
        'name', 'email', 'slack_ch', 'group'
    )

    search_fields = (
        'name',
    )

    autocomplete_fields = (
        'group',
    )


@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    """ [Admin] PENGUIN アカウント
    """
    fieldsets = (
        ('入力情報', {'fields': ('title', 'body')}),
        ('その他', {'fields': ('writer', 'update_datetime')}),
    )

    list_display = (
        'title', 'writer', 'update_datetime'
    )

    search_fields = (
        'title',
    )

    readonly_fields = (
        'update_datetime',
    )

    autocomplete_fields = (
        'writer',
    )


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    """ [Admin] お問い合わせ
    """
    fieldsets = (
        ('入力情報', {'fields': ('title', 'body', 'kind')}),
        ('その他', {'fields': ('writer', 'create_datetime')}),
    )

    list_display = (
        'title', 'kind', 'create_datetime'
    )

    search_fields = (
        'title',
    )

    readonly_fields = (
        'create_datetime',
    )

    autocomplete_fields = (
        'writer', 'kind'
    )


@admin.register(models.ContactKind)
class ContactKindAdmin(admin.ModelAdmin):
    """ [Admin] お問い合わせ種別
    """
    fieldsets = (
        (None, {'fields': ('name', 'office_groups')}),
    )

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )

    autocomplete_fields = (
        'office_groups',
    )
