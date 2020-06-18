from django.db import models


class Notice(models.Model):
    """ ホーム画面に表示される「お知らせ」
    """

    # settings

    class Meta:
        verbose_name = 'お知らせ'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # fields

    title = models.CharField(
        verbose_name='タイトル',
        max_length=30,
        help_text='30 文字以内で入力してください。'
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=100,
        help_text='100 文字以内で入力してください。URL を入力すると自動的にリンクに変換されます。'
    )

    writer = models.ForeignKey(
        'home.User',
        verbose_name='入力者',
        on_delete=models.SET_NULL,
        null=True
    )

    update_datetime = models.DateTimeField(
        verbose_name='最終更新日時',
        auto_now=True
    )
