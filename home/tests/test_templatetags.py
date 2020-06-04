from django.contrib.auth.models import Group
from django.test import TestCase

from home import models
from home.templatetags.get_notifications import GetNotifications


class GetNotificationsTestCase(TestCase):
    """[test] templatetsgs/get_notifications
    """

    def setUp(self):
        """各モデルを作成
        """

        # User
        user = models.User.objects.create_user(
            username='1000000000',
            email='a@a.com',
            shib_eptid='0',
            tel='0'
        )
        user_sender = models.User.objects.create_user(
            username='2000000000',
            email='b@b.com',
            shib_eptid='1',
            tel='1'
        )

        # Group
        group = Group.objects.create(
            name='グループ名'
        )

        # 通知（既読）
        # 最新 5 件のみ表示されるので read_notification_0 は表示されないはず
        self.read_notification_0 = models.Notification.objects.create(
            title='既読0（表示省略）',
            sender=user_sender,
            group=group
        )
        self.read_notification_0.to.add(user)
        models.NotificationRead.objects.create(
            notification=self.read_notification_0, user=user)

        self.read_notification_1 = models.Notification.objects.create(
            title='既読1',
            sender=user_sender,
            group=group
        )
        self.read_notification_1.to.add(user)
        models.NotificationRead.objects.create(
            notification=self.read_notification_1, user=user)

        self.read_notification_2 = models.Notification.objects.create(
            title='既読2',
            sender=user_sender,
            group=group
        )
        self.read_notification_2.to.add(user)
        models.NotificationRead.objects.create(
            notification=self.read_notification_2, user=user)

        self.read_notification_3 = models.Notification.objects.create(
            title='既読3',
            sender=user_sender,
            group=group
        )
        self.read_notification_3.to.add(user)
        models.NotificationRead.objects.create(
            notification=self.read_notification_3, user=user)

        # 通知（未読）
        self.unread_notification_0 = models.Notification.objects.create(
            title='未読0',
            sender=user_sender,
            group=group
        )
        self.unread_notification_0.to.add(user)

        self.unread_notification_1 = models.Notification.objects.create(
            title='未読1',
            sender=user_sender,
            group=group
        )
        self.unread_notification_1.to.add(user)

        # 通知（そもそも user に送られていない）
        self.not_receive_notification = models.Notification.objects.create(
            title='不受信',
            sender=user_sender,
            group=group
        )

        # context にログインユーザーを登録しておく
        self.context = {'user': user}

    def test_all_notification_list(self):
        """context['all_notification_list] の検証

        user あての通知を最新 5 件表示できていれば OK
        （表示は新しい順）
        """
        get_notifications = GetNotifications()
        get_notifications.render(self.context)

        self.assertEqual(
            list(self.context['all_notification_list']),
            [
                self.unread_notification_1,
                self.unread_notification_0,
                self.read_notification_3,
                self.read_notification_2,
                self.read_notification_1,
            ],
            '最新 5 件が正しく取得できていません'
        )

    def test_read_notification_list(self):
        """context['read_notification_list] の検証

        user あての既読通知を全て挙げられていれば
        """
        get_notifications = GetNotifications()
        get_notifications.render(self.context)

        self.assertEqual(
            list(self.context['read_notification_list']),
            [
                self.read_notification_0,
                self.read_notification_1,
                self.read_notification_2,
                self.read_notification_3,
            ],
            '既読通知が正しく取得できていません'
        )

    def test_unread_count(self):
        """context['unread_count'] の検証

        user あての未読件数を取得できれば OK
        """
        get_notifications = GetNotifications()
        get_notifications.render(self.context)

        self.assertEqual(
            self.context['unread_count'],
            2,
            '既読通知が正しく取得できていません'
        )
