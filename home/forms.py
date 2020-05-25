from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from home.models import User, UserToken


class UserTokenForm(forms.ModelForm):
    """PENGUIN アカウント（仮登録）
    """
    class Meta:
        model = UserToken
        fields = (
            'email',
        )

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            # すでにそのメールアドレスをもつユーザーがいる場合
            raise forms.ValidationError(
                'そのメールアドレスはすでに使用されています'
            )
        return data


class UserForm(UserCreationForm):
    """PENGUIN アカウント（本登録）
    """
    class Meta:
        model = User
        fields = (
            'username', "last_name", 'first_name',
            'last_name_kana', 'first_name_kana',
            'faculty', 'grade', 'tel',
            'password1', 'password2'
        )


class LoginForm(AuthenticationForm):
    """ログインフォーム

    エラーの表示方法を修正
    """

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                # 追加
                self.add_error('username', '')
                self.add_error('password', '')
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
