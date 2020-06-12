from django.db import models


class Notification(models.Model):
    """通知
    """

    # settings

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def has_read(self, user):
        """ある User がすでに通知を呼んだかどうかを判定する

        NotificationRead がヒットするかどうかを返す
        """
        return self.notificationread_set.filter(
            user=user
        ).exists()

    # fields

    title = models.CharField(
        verbose_name='表題',
        max_length=50
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=2000
    )

    to = models.ManyToManyField(
        'home.User',
        verbose_name='宛先',
        related_name='notification_to'
    )

    sender = models.ForeignKey(
        'home.User',
        verbose_name='送信者',
        on_delete=models.CASCADE,
        related_name='notification_from'
    )

    group = models.ForeignKey(
        'auth.Group',
        verbose_name='担当',
        on_delete=models.CASCADE,
        help_text='どの担当として送信するかをここで選択してください。',
    )

    create_datetime = models.DateTimeField(
        verbose_name='送信日時',
        auto_now_add=True
    )


class NotificationRead(models.Model):
    """通知既読情報
    """

    # settings

    class Meta:
        verbose_name = '通知既読'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.notification)

    # fields
    notification = models.ForeignKey(
        'home.Notification',
        verbose_name='通知',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'home.User',
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    create_datetime = models.DateTimeField(
        verbose_name='開封日時',
        auto_now_add=True
    )
