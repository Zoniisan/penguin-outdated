from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class Project(models.Model):
    """企画
    """

    class Meta:
        verbose_name = '企画'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.project_id:
            return '%s: %s' % (self.project_id, self.project_name)
        elif self.accept_id:
            return '%s: %s' % (self.submit_id, self.project_name)
        else:
            return self.project_name

    project_id = models.SlugField(
        verbose_name='企画コード',
        max_length=5,
        null=True
    )

    submit_id = models.SlugField(
        verbose_name='申請コード',
        max_length=5,
        null=True
    )

    registration = models.OneToOneField(
        'register.Registration',
        on_delete=models.CASCADE,
        verbose_name='登録データ'
    )

    leader = models.ForeignKey(
        'home.User',
        on_delete=models.CASCADE,
        verbose_name='責任者',
        related_name='project_leader'
    )

    member = models.ManyToManyField(
        'home.User',
        verbose_name='参加者',
        related_name='project_member'
    )

    project_name = models.CharField(
        verbose_name='企画名',
        max_length=100
    )

    project_name_kana = models.CharField(
        verbose_name='企画名（かな）',
        max_length=100
    )

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

    description = models.TextField(
        verbose_name='企画内容',
        max_length=1000
    )

    note = models.TextField(
        verbose_name='備考',
        max_length=1000,
        help_text='車両入構・マスコミの取材がある場合は入力してください'
    )

    # 企画詳細データとの関係
    detail_id = models.PositiveIntegerField()
    detail = GenericForeignKey('kind', 'detail_id')

    submit = models.BooleanField(
        verbose_name='提出',
        default=False
    )

    submit_datetime = models.DateTimeField(
        verbose_name='提出日時',
        null=True
    )

    accept = models.BooleanField(
        verbose_name='受理',
        default=False
    )

    accept_datetime = models.DateTimeField(
        verbose_name='受理日時',
        null=True
    )

    active = models.BooleanField(
        verbose_name='有効',
        default=False
    )
