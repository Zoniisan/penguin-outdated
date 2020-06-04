from django.contrib.auth.models import Group
from django.test import TestCase

from home import models


class UserTestCase(TestCase):
    """[test] User

    Model User のメソッドを検証する
    """
    def setUp(self):
        """User を作成
        """
        self.user = models.User.objects.create(
            username='1000000000',
            email='hoge@hoge.com',
            last_name='姓',
            first_name='名',
            last_name_kana='せい',
            first_name_kana='めい',
            faculty='総',
            grade='B1',
        )

    def test_str(self):
        """__str__ を検証

        get_display_name を同一の出力が出れば正解
        """
        self.assertEqual(
            str(self.user),
            '(総/B1) 姓名',
            (
                '__str__ の返り値が異常です。',
                'get_display_name の返り値と同じにしてください。'
            )
        )

    def test_get_full_name(self):
        """get_full_name を検証

        正解例: '姓名'
        """
        self.assertEqual(
            self.user.get_full_name(),
            '姓名',
            'get_full_name の返り値が異常です'
        )

    def test_get_display_name(self):
        """get_display_name を検証

        正解例: '(総/B1) 姓名'
        """
        self.assertEqual(
            self.user.get_display_name(),
            '(総/B1) 姓名',
            'get_display_name の返り値が異常です'
        )

    def test_get_username_and_name(self):
        """get_display_name を検証

        正解例: '姓名 (1000000000)'
        """
        self.assertEqual(
            self.user.get_username_and_name(),
            '姓名 (1000000000)',
            'get_username_and_name の返り値が異常です'
        )


class UserTokenTestCase(TestCase):
    """[test] UserToken

    Model UserToken のメソッドを検証する
    """
    def setUp(self):
        """UserToken を作成
        """
        self.user_token = models.UserToken.objects.create(
            email='hoge@hoge.com',
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.user_token),
            'hoge@hoge.com',
            (
                '__str__ の返り値が異常です。',
                'email を出力してください。'
            )
        )


class GroupInfoTestCase(TestCase):
    """[test] GroupInfo

    Model GroupInfo のメソッドを検証する
    """
    def setUp(self):
        """Group, GroupInfo を作成
        """
        group = Group.objects.create(
            name='グループ名'
        )

        self.group_info = models.GroupInfo.objects.create(
            group=group,
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.group_info),
            'グループ名',
            (
                '__str__ の返り値が異常です。',
                'group.name を出力してください。'
            )
        )


class NoticeTestCase(TestCase):
    """[test] Notice

    Model Notice のメソッドを検証する
    """
    def setUp(self):
        """Notice を作成
        """
        self.notice = models.Notice.objects.create(
            title='タイトル',
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.notice),
            'タイトル',
            (
                '__str__ の返り値が異常です。',
                'title を出力してください。'
            )
        )


class ContactTestCase(TestCase):
    """[test] Contact

    Model Contact のメソッドを検証する
    """
    def setUp(self):
        """Contact を作成
        """
        contact_kind = models.ContactKind.objects.create(
            name='hogehoge'
        )
        user = models.User.objects.create_user(
            username='1000000000'
        )

        self.contact = models.Contact.objects.create(
            title='タイトル',
            kind=contact_kind,
            writer=user
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.contact),
            'タイトル',
            (
                '__str__ の返り値が異常です。',
                'title を出力してください。'
            )
        )


class ContactKindTestCase(TestCase):
    """[test] ContactKind

    Model ContactKind のメソッドを検証する
    """
    def setUp(self):
        """Notice を作成
        """
        self.contact_kind = models.ContactKind.objects.create(
            name='種別名',
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.contact_kind),
            '種別名',
            (
                '__str__ の返り値が異常です。',
                'name を出力してください。'
            )
        )


class NotificationTestCase(TestCase):
    """[test] Notification

    Model Notification のメソッドを検証する
    """
    def setUp(self):
        """User, Notification, NotificationRead を作成
        """
        # Notification を受信し、既に読んだユーザー
        self.user_read_0 = models.User.objects.create_user(
            username='0000000000',
            email='a@a.com',
            tel='0',
            shib_eptid='0'
        )
        self.user_read_1 = models.User.objects.create_user(
            username='0000000001',
            email='b@b.com',
            tel='1',
            shib_eptid='1'
        )

        # Notification を受信し、まだ読んでいないユーザー
        self.user_unread_0 = models.User.objects.create_user(
            username='1000000000',
            email='c@c.com',
            tel='2',
            shib_eptid='2'
        )
        self.user_unread_1 = models.User.objects.create_user(
            username='1000000001',
            email='d@d.com',
            tel='3',
            shib_eptid='3'
        )

        # Notification を受信していないユーザー
        self.user_not_receive = models.User.objects.create_user(
            username='2000000000',
            email='e@e.com',
            tel='4',
            shib_eptid='4'
        )

        # Notification を送信したユーザー
        self.user_sender = models.User.objects.create_user(
            username='3000000000',
            email='f@f.com',
            tel='5',
            shib_eptid='5'
        )

        # 部局担当を作成
        group = Group.objects.create(
            name='部局担当'
        )

        # 通知
        self.notification = models.Notification.objects.create(
            title='タイトル',
            sender=self.user_sender,
            group=group
        )

        # 既読情報
        models.NotificationRead.objects.create(
            user=self.user_read_0,
            notification=self.notification
        )
        models.NotificationRead.objects.create(
            user=self.user_read_1,
            notification=self.notification
        )

        # 全く関係ない Notification を作成し、それを読んだ
        # ユーザーを 1 名想定する。
        another_notification = models.Notification.objects.create(
            title='別の通知',
            group=group,
            sender=self.user_unread_1
        )
        models.NotificationRead(
            notification=another_notification,
            user=self.user_unread_0
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.notification),
            'タイトル',
            (
                '__str__ の返り値が異常です。',
                'title を出力してください。'
            )
        )

    def test_has_read(self):
        """has_read を検証

        与えられた Notification に対応する
        NotificationRead が登録されているユーザーについては True,
        そうでなければ False を返せば良い。
        """
        self.assertTrue(
            self.notification.has_read(self.user_read_0),
            '既読ユーザーの既読記録を読み込めていません'
        )
        self.assertTrue(
            self.notification.has_read(self.user_read_1),
            '既読ユーザーの既読記録を読み込めていません'
        )
        self.assertFalse(
            self.notification.has_read(self.user_unread_0),
            '別の通知の既読記録を誤って読み込んでいます'
        )
        self.assertFalse(
            self.notification.has_read(self.user_unread_1),
            '既読記録のないユーザーを誤って読み込んでいます'
        )
        self.assertFalse(
            self.notification.has_read(self.user_not_receive),
            '送信先でないユーザーを誤って読み込んでいます'
        )
        self.assertFalse(
            self.notification.has_read(self.user_sender),
            '送信者を誤って読み込んでいます'
        )


class NotificationReadTestCase(TestCase):
    """[test] NotificationRead

    Model NotificationRead のメソッドを検証する
    """
    def setUp(self):
        """User, Notice, NotificationRead を作成
        """
        user_read = models.User.objects.create_user(
            username='1000000000',
            email='a@a.com',
            tel='0',
            shib_eptid='0'
        )

        user_send = models.User.objects.create_user(
            username='2000000000',
            email='b@b.com',
            tel='1',
            shib_eptid='1'
        )

        group = Group.objects.create(
            name='グループ名'
        )

        notification = models.Notification.objects.create(
            title='タイトル',
            sender=user_send,
            group=group
        )

        self.notification_read = models.NotificationRead.objects.create(
            notification=notification,
            user=user_read
        )

    def test_str(self):
        """__str__ を検証
        """
        self.assertEqual(
            str(self.notification_read),
            'タイトル',
            (
                '__str__ の返り値が異常です。',
                'str(notification) = notification.title を出力してください。'
            )
        )
