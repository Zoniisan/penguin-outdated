from django.db import models


class PeriodBase(models.Model):
    """Period 系 モデルの基礎
    """
    # settings
    def __str__(self):
        return '-'.join([str(self.start), str(self.finish)])

    # fields
    start = models.DateTimeField(
        verbose_name='開始'
    )

    finish = models.DateTimeField(
        verbose_name='終了'
    )
