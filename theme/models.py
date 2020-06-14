from django.core.validators import MinLengthValidator
from django.db import models


class Theme(models.Model):
    """ 統一テーマ案
    """
    class Meta:
        verbose_name = '統一テーマ案'
        verbose_name_plural = verbose_name
        ordering = ('pk',)

    def __str__(self):
        return self.theme

    def first_count(self):
        """予選投票の票数を取得
        """
        return self.firstvote_set.count()

    def final_count(self):
        """決選投票の票数を取得
        """
        return self.finalvote_set.count()

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
        help_text='受理した場合のみ入力',
        max_length=6,
        null=True, blank=True
    )

    final_id = models.CharField(
        verbose_name='決選コード',
        help_text='決選進出した場合のみ入力',
        max_length=6,
        null=True, blank=True
    )


class FirstVoteEptid(models.Model):
    """予選投票 EPTID 記録用のモデル

    eptid を pk とし、作成日時（作成順）をわからなくすることで匿名性を保持
    """
    class Meta:
        verbose_name = '予選投票/EPTID'
        verbose_name_plural = verbose_name
        ordering = ('eptid',)

    def __str__(self):
        return self.eptid

    eptid = models.CharField(
        verbose_name='eptid',
        max_length=400,
        primary_key=True
    )


class FinalVoteEptid(models.Model):
    """決選投票 EPTID 記録用のモデル

    eptid を pk とし、作成日時（作成順）をわからなくすることで匿名性を保持
    """
    class Meta:
        verbose_name = '決選投票/EPTID'
        verbose_name_plural = verbose_name
        ordering = ('eptid',)

    def __str__(self):
        return self.eptid

    eptid = models.CharField(
        verbose_name='eptid',
        max_length=400,
        primary_key=True
    )


class FirstVote(models.Model):
    class Meta:
        verbose_name = '予選投票/投票先'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.theme)

    theme = models.ForeignKey(
        'theme.Theme',
        verbose_name='統一テーマ案',
        on_delete=models.CASCADE
    )


class FinalVote(models.Model):
    class Meta:
        verbose_name = '決選投票/投票先'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.theme)

    theme = models.ForeignKey(
        'theme.Theme',
        verbose_name='統一テーマ案',
        on_delete=models.CASCADE
    )
