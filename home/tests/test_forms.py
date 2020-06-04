from django.test import TestCase

from home.forms import LoginForm, UserTokenForm
from home.models import User, UserToken


class UserTokenFormTestCase(TestCase):
    """[test] UserTokenForm

    clean_email を検証する
    """
    def setUp(self):
        """User を作成
        """
        # User を作成
        # これが作成された時点で email = hoge@hoge.com の
        # UserToken は作成できなくなる。
        User.objects.create_user(
            username='1000000000',
            email='hoge@hoge.com',
            password='password',
        )

        # User を作成
        # これが作成されても email = fuga@fuga.com の
        # UserToken は作成できる。
        # （email = fuga@fuga.com の User が存在しないため）
        UserToken.objects.create(
            email='fuga@fuga.com',
            token='token'
        )

    def test_user_created(self):
        """同一の email をもつ User が既に作成されている場合 →失敗

        既に同一の email を持つ User が存在する場合は、
        UserToken を作成することはできない。
        """
        # create form data
        data = {
            'email': 'hoge@hoge.com'
        }
        form = UserTokenForm(data=data)
        self.assertFalse(form.is_valid())

    def test_usertoken_created(self):
        """同一の email をもつ UserToken が既に作成されている場合 →成功

        既に同一の email を持つ UserToken が存在する場合は、
        同一の email をもつ User が存在しなければ、
        UserToken を作成することができる。
        """
        # create form data
        data = {
            'email': 'fuga@fuga.com'
        }
        form = UserTokenForm(data=data)
        self.assertTrue(form.is_valid())


class LoginFormTestCase(TestCase):
    """[test] LoginForm

    正しい学生番号とパスワードでログインできるかどうかを確認。
    また失敗した場合は username と password の両方に
    エラーが登録されているかどうかを確認する。
    """
    def setUp(self):
        """User を作成
        """
        # User を作成
        User.objects.create_user(
            username='1000000000',
            email='hoge@hoge.com',
            password='password'
        )

    def test_login_successful(self):
        """学生番号・パスワード一致 -- 成功
        """
        # create form data
        data = {
            'username': '1000000000',
            'password': 'password'
        }
        form = LoginForm(data=data)

        # ログイン成功
        self.assertTrue(
            form.is_valid(),
            '正しい学生番号とパスワードでログインできません'
        )

    def test_mistake_username(self):
        """学生番号誤り・パスワード一致 -- 失敗

        学生番号・パスワードの両方にエラー表示を行う
        """
        # create form data
        data = {
            'username': '9999999999',
            'password': 'password'
        }
        form = LoginForm(data=data)

        # ログイン失敗
        self.assertFalse(
            form.is_valid(),
            '誤った学生番号でログインできました'
        )

        # 学生番号・パスワードの両方にエラー表示
        self.assertTrue(
            'username' in form.errors,
            '学生番号誤り -- 学生番号にエラーが表示されていません'
        )
        self.assertTrue(
            'password' in form.errors,
            '学生番号誤り -- パスワードにエラーが表示されていません'
        )

    def test_mistake_password(self):
        """学生番号一致・パスワード誤り -- 失敗

        学生番号・パスワードの両方にエラー表示を行う
        """
        # create form data
        data = {
            'username': '1000000000',
            'password': 'mistake'
        }
        form = LoginForm(data=data)

        # ログイン失敗
        self.assertFalse(
            form.is_valid(),
            '誤ったパスワードでログインできました'
        )

        # 学生番号・パスワードの両方にエラー表示
        self.assertTrue(
            'username' in form.errors,
            'パスワード誤り -- 学生番号にエラーが表示されていません'
        )
        self.assertTrue(
            'password' in form.errors,
            'パスワード誤り -- パスワードにエラーが表示されていません'
        )

    def test_mistake_both(self):
        """学生番号誤り・パスワード誤り -- 失敗

        学生番号・パスワードの両方にエラー表示を行う
        """
        # create form data
        data = {
            'username': '9999999999',
            'password': 'mistake'
        }
        form = LoginForm(data=data)

        # ログイン失敗
        self.assertFalse(
            form.is_valid(),
            '誤った学生番号・パスワードでログインできました'
        )

        # 学生番号・パスワードの両方にエラー表示
        self.assertTrue(
            'username' in form.errors,
            '学生番号・パスワード誤り -- 学生番号にエラーが表示されていません'
        )
        self.assertTrue(
            'password' in form.errors,
            '学生番号・パスワード誤り -- パスワードにエラーが表示されていません'
        )
