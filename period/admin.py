from django.contrib import admin

from period import models


class PeriodAdmin(admin.ModelAdmin):
    """Period 系モデルの管理サイトを定義
    """
    list_display = (
        'start', 'finish'
    )


admin.site.register(models.PeriodeThemeSubmit)
admin.site.register(models.PeriodeThemeFirstVote)
admin.site.register(models.PeriodeThemeFinalVote)
