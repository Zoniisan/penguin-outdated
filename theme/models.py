from django.core.validators import MinLengthValidator
from django.db import models

from home.models import PeriodBase


class Theme(models.Model):
    # settings
    class Meta:
        verbose_name = '統一テーマ案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.theme

    # fields
    theme = models.CharField(
        verbose_name='統一テーマ',
        max_length=100
    )

    description = models.CharField(
        verbose_name='趣意文',
        max_length=400,
        validators=[MinLengthValidator(100)]
    )

    writer = models.OneToOneField(
        'home.User',
        verbose_name='応募者',
        on_delete=models.CASCADE
    )

    create_datetime = models.DateTimeField(
        verbose_name='応募日時',
        auto_now_add=True
    )

    accepted = models.BooleanField(
        verbose_name='受理',
        default=False
    )

    final = models.BooleanField(
        verbose_name='決勝進出',
        default=False
    )


class FirstVote(models.Model):
    # settings
    class Meta:
        verbose_name = '予選投票'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.theme)

    # fields
    theme = models.ForeignKey(
        'theme.Theme',
        verbose_name='投票',
        on_delete=models.CASCADE
    )

    eptid = models.CharField(
        verbose_name='投票者 eptid',
        max_length=400,
        unique=True
    )

    vote_datetime = models.DateTimeField(
        verbose_name='投票日時',
        auto_now_add=True
    )


class FinalVote(models.Model):
    # settings
    class Meta:
        verbose_name = '決戦投票'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.theme)

    # fields
    theme = models.ForeignKey(
        'theme.Theme',
        verbose_name='投票',
        on_delete=models.CASCADE
    )

    eptid = models.CharField(
        verbose_name='投票者 eptid',
        max_length=400,
        unique=True
    )

    vote_datetime = models.DateTimeField(
        verbose_name='投票日時',
        auto_now_add=True
    )


class PeriodApplication(PeriodBase):
    # settings
    class Meta:
        verbose_name = 'テーマ案募集期間'
        verbose_name_plural = verbose_name
        ordering = ('start',)


class PeriodFirstVote(PeriodBase):
    # settings
    class Meta:
        verbose_name = '予選投票期間'
        verbose_name_plural = verbose_name
        ordering = ('start',)


class PeriodFinalVote(PeriodBase):
    # settings
    class Meta:
        verbose_name = '決選投票期間'
        verbose_name_plural = verbose_name
        ordering = ('start',)
