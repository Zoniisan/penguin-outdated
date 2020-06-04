from django.conf import settings
from django.core import mail
from django.test import TestCase

from home import models
from home.tasks import send_mail_async


class SendMailAsyncTest(TestCase):
    """[test] send_mail_async
    """
    def setUp(self):
        pass

    def test_send_mail_async(self):
        """send_mail_async を検証
        """
        # 受信ユーザー作成
        user_receive_0 = models.User.objects.create_user(
            username='0000000000',
            email='a@a.com',
            tel='0',
            shib_eptid='0'
        )
        user_receive_1 = models.User.objects.create_user(
            username='0000000001',
            email='b@b.com',
            tel='1',
            shib_eptid='1'
        )

        send_mail_async(
            'タイトル',
            '本文',
            [user_receive_0, user_receive_1]
        )

        # メールの送信を確認
        self.assertEqual(
            len(mail.outbox),
            1,
            'メールが送信されていません'
        )

        # 件名
        self.assertEqual(
            mail.outbox[0].subject,
            'タイトル',
            'subject が不正です'
        )

        # 本文
        self.assertEqual(
            mail.outbox[0].body,
            '本文',
            'body が不正です'
        )

        # 差出人
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.EMAIL_HOST_USER,
            'from_email が不正です'
        )

        # 宛先
        self.assertEqual(
            mail.outbox[0].to,
            [user_receive_0, user_receive_1],
            'to が不正です'
        )
