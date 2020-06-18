from django.contrib import admin

from period import models


class PeriodAdmin(admin.ModelAdmin):
    """Period 系モデルの管理サイトを定義
    """
    list_display = (
        'start', 'finish'
    )


admin.site.register(models.PeriodThemeSubmit, PeriodAdmin)
admin.site.register(models.PeriodThemeFirstVote, PeriodAdmin)
admin.site.register(models.PeriodThemeFinalVote, PeriodAdmin)
