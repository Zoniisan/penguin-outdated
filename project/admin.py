from django.contrib import admin

from project import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    """ [Admin] 企画
    """

    fieldsets = (
        ('コード', {'fields': ('project_id', 'submit_id')}),
        ('登録データ', {'fields': ('registration',)}),
        ('ユーザー情報', {'fields': ('leader', 'member')}),
        ('企画情報', {'fields': (
            'project_name', 'project_name_kana',
            'group_name', 'group_name_kana',
            'kind', 'food', 'description', 'note'
        )}),
        ('企画詳細情報', {'fields': ('detail_id',)}),
        ('状態', {'fields': (
            'submit', 'submit_datetime', 'accept', 'accept_datetime'
        )}),
    )

    list_display = (
        'project_name', 'leader', 'kind', 'submit_id', 'project_id',
        'submit', 'accept'
    )

    search_fields = (
        'project_name', 'project_name_kana', 'submit_id', 'project_id'
    )

    autocomplete_fields = (
        'registration', 'leader', 'member'
    )
