from django.db import models


class AbstractPeriod(models.Model):
    """Period 系 model は各手続きが行える期間を定義する

    start, finish の期間内に現在時刻が含まれていれば有効
    複数インスタンスが存在する場合は、そのうちどれかに含まれていれば有効
    """
    class Meta:
        ordering = ('start',)

    def __str__(self):
        return '-'.join([self.start, self.finish])

    start = models.DateTimeField(
        verbose_name='開始日時'
    )

    finish = models.DateTimeField(
        verbose_name='終了日時'
    )


class PeriodeThemeSubmit(AbstractPeriod):
    class Meta:
        verbose_name = '統一テーマ応募期間'
        verbose_name_plural = verbose_name


class PeriodeThemeFirstVote(AbstractPeriod):
    class Meta:
        verbose_name = '統一テーマ予選投票期間'
        verbose_name_plural = verbose_name


class PeriodeThemeFinalVote(AbstractPeriod):
    class Meta:
        verbose_name = '統一テーマ決選投票期間'
        verbose_name_plural = verbose_name
