from django.contrib import admin

from theme import models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    """ [Admin] 統一テーマ案
    """
    fieldsets = (
        ('応募内容', {'fields': ('theme', 'description')}),
        ('応募者情報', {'fields': (
            'writer',
        )}),
        ('状態', {'fields': (
            'create_datetime', 'accepted', 'final'
        )}),
    )

    list_display = (
        'theme', 'writer', 'create_datetime', 'accepted', 'final'
    )

    search_fields = (
        'theme',
    )

    autocomplete_fields = (
        'writer',
    )

    list_filter = (
        'accepted', 'final'
    )

    readonly_fields = (
        'create_datetime',
    )


@admin.register(models.FirstVote)
class FirstVoteAdmin(admin.ModelAdmin):
    """ [Admin] 予選投票
    """
    fieldsets = (
        (None, {'fields': ('theme', 'eptid', 'vote_datetime')}),
    )

    list_display = (
        'theme', 'vote_datetime'
    )

    autocomplete_fields = (
        'theme',
    )

    readonly_fields = (
        'vote_datetime',
    )


@admin.register(models.FinalVote)
class FinalVoteAdmin(admin.ModelAdmin):
    """ [Admin] 決戦投票
    """
    fieldsets = (
        (None, {'fields': ('theme', 'eptid', 'vote_datetime')}),
    )

    list_display = (
        'theme', 'vote_datetime'
    )

    autocomplete_fields = (
        'theme',
    )

    readonly_fields = (
        'vote_datetime',
    )


@admin.register(models.PeriodApplication)
class PeriodApplicationAdmin(admin.ModelAdmin):
    """ [Admin] テーマ案募集期間
    """
    fieldsets = (
        (None, {'fields': ('start', 'finish')}),
    )

    list_display = (
        'start', 'finish'
    )


@admin.register(models.PeriodFirstVote)
class PeriodFirstVoteAdmin(admin.ModelAdmin):
    """ [Admin] 予選投票期間
    """
    fieldsets = (
        (None, {'fields': ('start', 'finish')}),
    )

    list_display = (
        'start', 'finish'
    )


@admin.register(models.PeriodFinalVote)
class PeriodFinalVoteAdmin(admin.ModelAdmin):
    """ [Admin] 決選投票期間
    """
    fieldsets = (
        (None, {'fields': ('start', 'finish')}),
    )

    list_display = (
        'start', 'finish'
    )
