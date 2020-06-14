from django.contrib import admin
from theme import models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    """ [Admin] 統一テーマ案
    """

    def first_count(self, obj):
        """予選投票の票数を表示
        """
        return obj.first_count()
    first_count.short_description = '予選投票/票数'

    def final_count(self, obj):
        """決選投票の票数を表示
        """
        return obj.final_count()
    final_count.short_description = '決選投票/票数'

    fieldsets = (
        ('応募内容', {'fields': (
            'theme', 'description', 'writer', 'create_datetime'
        )}),
        ('状況', {'fields': (
            'first_id', 'first_count', 'final_id', 'final_count'
        )}),
    )

    list_display = (
        'theme', 'create_datetime', 'first_id', 'first_count',
        'final_id', 'final_count'
    )

    search_fields = (
        'theme',
    )

    autocomplete_fields = (
        'writer',
    )

    readonly_fields = (
        'create_datetime', 'first_count', 'final_count'
    )


class EptidAdmin(admin.ModelAdmin):
    """EPTID 記録用の admin
    """
    list_display = (
        'eptid',
    )


admin.site.register(models.FirstVoteEptid, EptidAdmin)
admin.site.register(models.FinalVoteEptid, EptidAdmin)


class VoteAdmin(admin.ModelAdmin):
    """Vote 記録用の admin
    """
    list_display = (
        'theme',
    )

    autocomplete_fields = (
        'theme',
    )

admin.site.register(models.FirstVote, VoteAdmin)
admin.site.register(models.FinalVote, VoteAdmin)
