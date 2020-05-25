import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from home import forms
from home.models import Notice, User, UserToken
from penguin import mixins


class IndexView(generic.TemplateView):
    """ホーム画面
    """

    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Notice（お知らせ）を表示
        context['notice_list'] = Notice.objects.all()
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
        form.instance.token = ''.join(
            random.choices(string.ascii_letters + string.digits, k=100)
        )

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
        message = render_to_string('home/mails/signup_token.txt', context)
        from_email = 'penguin.nfoffice@gmail.com'
        recipient_list = [form.cleaned_data['email']]
        send_mail(subject, message, from_email, recipient_list)

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
        user_token = UserToken.objects.get(token=self.kwargs['token'])
        context['email'] = user_token.email
        return context

    def form_valid(self, form):
        user_token = UserToken.objects.get(token=self.kwargs['token'])

        # メールアドレス登録
        form.instance.email = user_token.email

        # 以下は shibboleth が導入されるまでの暫定的措置
        # eptid はランダム生成
        form.instance.shib_eptid = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        # affiliation は一律 student
        form.instance.shib_affiliation = 'student'

        # トークン無効化
        user_token.used = True
        user_token.save()

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


class NoticeView(mixins.AdminOnlyMixin, generic.CreateView):
    """お知らせ管理画面

    システム管理者のみ利用可能
    """

    template_name = 'home/notice.html'
    fields = ('title', 'body')
    model = Notice
    success_url = reverse_lazy('home:notice')

    def form_valid(self, form):
        # writer を登録
        form.instance.writer = self.request.user

        # message 発出
        messages.success(
            self.request, 'お知らせ「%s」を登録しました！' %
            form.instance.title
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice_list'] = Notice.objects.all()
        return context


def notice_delete(self, pk):
    """お知らせを削除

    システム管理者のみ利用可能
    """
    # admin only
    if not self.user.is_superuser:
        raise PermissionDenied

    notice = Notice.objects.get(pk=pk)
    notice.delete()
    messages.error(self, 'お知らせ「%s」を削除しました！' % notice.title)
    return redirect('home:notice')


class NoticeUpdateView(mixins.AdminOnlyMixin, generic.UpdateView):
    """お知らせ更新画面

    システム管理者のみ利用可能
    """

    template_name = 'home/notice_update.html'
    fields = ('title', 'body')
    model = Notice
    success_url = reverse_lazy('home:notice')

    def form_valid(self, form):
        # writer を登録
        form.instance.writer = self.request.user

        # message 発出
        messages.success(
            self.request, 'お知らせ「%s」を更新しました！' %
            form.instance.title
        )

        return super().form_valid(form)
