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


@admin.register(models.GroupInfo)
class GroupInfoAdmin(admin.ModelAdmin):
    """ [Admin] 部局担当
    """

    def group_name(self, obj):
        """対応する auth.Group の名前を取得

        OneToOneField の参照先のフィールドは
        このような関数を作って参照しなければならない。
        """
        return obj.group.name
    group_name.short_description = '部局担当名'

    fieldsets = (
        ('基本情報', {'fields': ('email', 'slack_ch')}),
        ('auth.Group との関連', {'fields': ('group',)}),
    )

    list_display = (
        'group_name', 'email', 'slack_ch', 'group'
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
        (None, {'fields': ('name', 'groups')}),
    )

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )

    autocomplete_fields = (
        'groups',
    )


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ [Admin] 通知
    """
    fieldsets = (
        ('内容', {'fields': ('title', 'body', 'group')}),
        ('送受信情報', {'fields': ('to', 'sender', 'create_datetime')}),
    )

    list_display = (
        'title', 'sender', 'group', 'create_datetime'
    )

    search_fields = (
        'title',
    )

    autocomplete_fields = (
        'to', 'sender'
    )

    readonly_fields = (
        'create_datetime',
    )


@admin.register(models.NotificationRead)
class NotificationReadAdmin(admin.ModelAdmin):
    """ [Admin] 通知既読
    """
    fieldsets = (
        ('None', {'fields': ('notification', 'user', 'create_datetime')}),
    )

    list_display = (
        'notification', 'user', 'create_datetime'
    )

    search_fields = (
        'notification',
    )

    autocomplete_fields = (
        'notification', 'user'
    )

    readonly_fields = (
        'create_datetime',
    )
