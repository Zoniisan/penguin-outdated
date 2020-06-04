from django.test import TestCase
from home.models import User
from django.core.management import call_command


class CreateManyUsersTestCase(TestCase):
    """[test] command: create_many_users

    manage.py コマンド create_many_users を検証する
    """
    def setUp(self):
        """manage.py create_many_users 実行
        """
        call_command('create_many_users')

    def test_create_student(self):
        """アカウントの作成状況を確認する
        """
        # 一般ユーザー（生徒）作成確認
        self.assertTrue(
            User.objects.filter(
                username='1000000099',
                is_staff=False,
                is_superuser=False,
                shib_affiliation='student'
            ).exists(),
            '一般ユーザー（生徒）が正しく作成されていません。'
        )

        # 一般ユーザー（教授陣）作成確認
        self.assertTrue(
            User.objects.filter(
                username='2000000099',
                is_staff=False,
                is_superuser=False,
                shib_affiliation='faculty'
            ).exists(),
            '一般ユーザー（教授）が正しく作成されていません。'
        )

        # 事務局員作成確認
        # この時点では is_staff = False とすること！！
        # （実際のスタッフ登録は CSV 処理で行います）
        self.assertTrue(
            User.objects.filter(
                username='3000000099',
                is_staff=False,
                is_superuser=False,
                shib_affiliation='student'
            ).exists(),
            (
                '事務局員が正しく作成されていません'
                '（この時点では is_staff = False とすること！）'
            )
        )
