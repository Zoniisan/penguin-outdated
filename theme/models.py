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

    # functions
    def first_accepted(self):
        return self.first_id is not None

    def final_accepted(self):
        return self.final_id is not None

    def first_count(self):
        return self.firstvote_set.all().count()

    def final_count(self):
        return self.finalvote_set.all().count()

    # fields
    theme = models.CharField(
        verbose_name='統一テーマ',
        max_length=100,
        help_text='1 文字以上 100 文字以下で入力してください。'
    )

    description = models.TextField(
        verbose_name='趣意文',
        max_length=400,
        validators=[MinLengthValidator(100)],
        help_text='100 文字以上 400 文字以下で入力してください。'
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

    first_id = models.CharField(
        verbose_name='予選コード',
        max_length=6,
        null=True, blank=True
    )

    final_id = models.CharField(
        verbose_name='決選コード',
        max_length=6,
        null=True, blank=True
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
