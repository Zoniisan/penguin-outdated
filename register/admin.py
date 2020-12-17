from django.contrib import admin

from register import models


@admin.register(models.Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """ [Admin] 企画登録
    """

    fieldsets = (
        ('入力情報', {'fields': (
            'group_name', 'group_name_kana', 'short_description'
        )}),
        ('企画情報', {'fields': ('kind', 'food')}),
        ('呼び出し情報', {'fields': ('status', 'call_id')}),
        ('登録情報', {'fields': (
            'token', 'register_datetime', 'registerant', 'staff'
        )}),
    )

    list_display = (
        'group_name', 'status', 'call_id', 'registerant'
    )

    search_fields = (
        'group_name', 'group_name_kana'
    )

    autocomplete_fields = (
        'registerant', 'staff',
    )
