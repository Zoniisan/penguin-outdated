from django.db import models


class Registration(models.Model):
    """企画登録
    """

    class Meta:
        verbose_name = '企画登録'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name

    group_name = models.CharField(
        verbose_name='団体名',
        max_length=100
    )

    group_name_kana = models.CharField(
        verbose_name='団体名（かな）',
        max_length=100
    )

    kind = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        verbose_name='企画種別'
    )

    food = models.BooleanField(
        verbose_name='飲食物提供',
        default=False
    )

    short_description = models.CharField(
        verbose_name='企画概要',
        max_length=100,
        help_text='簡潔に内容を説明してください。暫定的な内容で構いません。'
    )

    call_id = models.SlugField(
        verbose_name='呼び出しコード',
        max_length=4
    )

    status_choices = (
        ('waiting', '待機中'),
        ('calling', '呼出中'),
        ('handling', '対応中'),
        ('accepted', '登録完了'),
        ('invalid', '無効')
    )

    status = models.CharField(
        verbose_name='状態',
        max_length=10,
        choices=status_choices,
        default='waiting'
    )

    token = models.CharField(
        verbose_name='トークン',
        max_length=50,
        null=True
    )

    register_datetime = models.DateTimeField(
        verbose_name='登録完了日時',
        null=True
    )

    registerant = models.ForeignKey(
        'home.User',
        verbose_name='登録者',
        on_delete=models.CASCADE,
        related_name='registration_registerant'
    )

    staff = models.ForeignKey(
        'home.User',
        verbose_name='登録スタッフ',
        on_delete=models.CASCADE,
        related_name='registration_staff'
    )
