from django.db import models


class Contact(models.Model):
    """お問い合わせ
    """

    # settings

    class Meta:
        verbose_name = 'お問い合わせ'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # fields
    title = models.CharField(
        verbose_name='表題',
        max_length=100
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=2000
    )

    kind = models.ForeignKey(
        'home.ContactKind',
        verbose_name='お問い合わせ種別',
        on_delete=models.CASCADE
    )

    writer = models.ForeignKey(
        'home.User',
        verbose_name='入力者',
        on_delete=models.CASCADE
    )

    create_datetime = models.DateTimeField(
        verbose_name='作成日時',
        auto_now_add=True
    )


class ContactKind(models.Model):
    """お問い合わせ種別
    """

    # settings

    class Meta:
        verbose_name = 'お問い合わせ種別'
        verbose_name_plural = verbose_name
        ordering = ('order',)

    def __str__(self):
        return self.name

    # fields

    name = models.CharField(
        verbose_name='種別名',
        max_length=100
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='管轄'
    )

    order = models.PositiveIntegerField(
        default=0
    )
