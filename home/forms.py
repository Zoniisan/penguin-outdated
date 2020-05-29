from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_select2 import forms as s2forms

from home.models import Notification, User, UserToken


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


class NotificationToWidget(s2forms.ModelSelect2MultipleWidget):
    """通知フォーム/宛先選択 Widget
    """
    search_fields = [
        'username__icontains',
        'last_name__icontains',
        'first_name__icontains',
        'last_name_kana__icontains',
        'first_name_kana__icontains',
        'email__icontains',
    ]


class NotificationForm(forms.ModelForm):
    """通知フォーム
    """
    class Meta:
        model = Notification
        fields = (
            'to', 'title', 'body', 'group'
        )
        widgets = {
            "to": NotificationToWidget(
                attrs={
                    'data-placeholder': '選択して宛先を入力',
                }
            ),
        }
