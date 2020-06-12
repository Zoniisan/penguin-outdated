from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from home import forms
from home.models import User, UserToken
from home.tasks import send_mail_async
from home.views.helper import (craete_random_strings, get_staff_member_list,
                               register_notice_list_to_context)
from penguin import mixins


class IndexView(generic.TemplateView):
    """ホーム画面
    """

    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Notice（お知らせ）を表示
        register_notice_list_to_context(context)

        return context


class SignUpTokenView(generic.CreateView):
    """signup: 仮登録画面
    """

    template_name = 'home/signup_token.html'
    form_class = forms.UserTokenForm
    model = UserToken
    success_url = reverse_lazy('home:signup_token_finish')

    def form_valid(self, form):
        # token を生成
        form.instance.token = craete_random_strings()

        # email を送信
        subject = 'PENGUIN アカウント仮登録完了'
        context = {
            'base_url': settings.BASE_URL,
            'signup_url': '/'.join([
                str(reverse_lazy(
                    'home:signup', kwargs={'token': form.instance.token}
                ))
            ]),
        }
        body = render_to_string('home/mails/signup_token.txt', context)
        to_list = [form.cleaned_data['email']]
        send_mail_async.delay(
            subject,
            body,
            to_list
        )

        return super().form_valid(form)


class SignUpTokenFinishView(generic.TemplateView):
    """signup: 仮登録完了画面
    """

    template_name = 'home/signup_token_finish.html'


class SignUpView(generic.CreateView):
    """signup: 本登録画面
    """

    template_name = 'home/signup.html'
    model = User
    form_class = forms.UserForm
    success_url = reverse_lazy('home:signup_finish')

    def get(self, request, **kwargs):
        # トークンの検証
        try:
            user_token = UserToken.objects.get(token=self.kwargs['token'])
        except UserToken.DoesNotExist:
            # トークンが存在しない場合
            messages.error(request, 'このリンクは無効です。アドレスを間違えていませんか？')
            return redirect('home:index')

        if user_token.used:
            # トークン使用済み
            messages.error(request, 'このリンクは使用済みです。アカウント仮登録からやり直してください。')
            return redirect('home:signup_token')
        if datetime.now() > user_token.create_datetime + timedelta(hours=1):
            # 有効期限切れ（1 時間超過）
            messages.error(request, 'このリンクは有効期限切れです。アカウント仮登録からやり直してください。')
            return redirect('home:signup_token')

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # UserToken を取得
        user_token = UserToken.objects.get(token=self.kwargs['token'])

        # Email を UserToken.email から取得
        context['email'] = user_token.email

        return context

    def form_valid(self, form):
        user_token = UserToken.objects.get(token=self.kwargs['token'])

        # メールアドレス登録
        form.instance.email = user_token.email

        # 以下は shibboleth が導入されるまでの暫定的措置
        # eptid はランダム生成
        form.instance.shib_eptid = craete_random_strings(10)

        # affiliation は一律 student
        form.instance.shib_affiliation = 'student'

        # トークン無効化
        user_token.used = True
        user_token.save()

        # save
        self.object = form.save()

        # email を送信
        subject = 'PENGUIN アカウント本登録完了'
        context = {
            'base_url': settings.BASE_URL,
            'user': self.object
        }
        body = render_to_string('home/mails/signup_finish.txt', context)
        to_list = [self.object.email]
        send_mail_async.delay(
            subject,
            body,
            to_list
        )

        return super().form_valid(form)


class SignUpFinishView(generic.TemplateView):
    """signup: 本登録完了画面
    """

    template_name = 'home/signup_finish.html'


class LoginView(AuthLoginView):
    """ログイン画面
    """

    template_name = 'home/login.html'
    form_class = forms.LoginForm

    def form_valid(self, form):
        messages.success(self.request, 'ログイン成功しました！')
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    """ログアウト画面
    """

    template_name = 'home/logout.html'


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """プロフィール画面
    """

    template_name = 'home/profile.html'


class StaffListView(mixins.StaffOnlyMixin, generic.TemplateView):
    """事務局員名簿
    """

    template_name = 'home/staff_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 事務局員名簿を作成
        # 部局担当別、学年・氏名読みがな順でリストを作成
        context['object_list'] = get_staff_member_list()

        return context


def download_staff_vcards(request, mode):
    """事務局員の連絡先を vcard 形式でダウンロード
    """

    # アクセスはスタッフのみ
    if not request.user.is_staff:
        raise PermissionDenied

    # URL から受け取ったモードに基づきデータをフィルタリング
    if mode == 'all':
        user_list = User.objects.filter(is_staff=True)
    elif mode == 'b1':
        user_list = User.objects.filter(is_staff=True, grade='B1')
    elif mode == 'b2':
        user_list = User.objects.filter(is_staff=True, grade='B2')
    elif mode == 'b3':
        user_list = User.objects.filter(is_staff=True, grade='B3')

    # vcf ファイル作成
    context = {
        'user_list': user_list
    }
    content = render_to_string(
        'home/others/vcards_template.txt', context
    )

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content, content_type='text/x-vcard')
    response['Content-Disposition'] = \
        'attachment; filename="nfoffice_vcards.vcf"'

    return response
