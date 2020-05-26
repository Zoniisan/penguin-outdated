import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django_slack import slack_message

from home import forms
from home.models import Contact, ContactKind, Notice, User, UserToken
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
        from_email = settings.EMAIL_HOST_USER
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

    notice = get_object_or_404(Notice, pk=pk)
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


class ContactView(LoginRequiredMixin, generic.CreateView):
    """お問い合わせ作成画面

    要ログイン
    """

    template_name = 'home/contact.html'
    fields = ('kind', 'title', 'body')
    model = Contact
    success_url = reverse_lazy('home:contact')

    def form_valid(self, form):
        # writer を登録
        form.instance.writer = self.request.user

        # save
        self.object = form.save()

        # お問い合わせの種類に応じた管轄部局に slack を送る
        for office_group in form.instance.kind.office_groups.all():
            context = {
                'office_group': office_group,
            }
            attachments = [{
                "fallback": "お問い合わせ内容",
                "color": "#2ed0d9",
                "fields": [
                    {
                        "title": "種別",
                        "value": form.instance.kind.name,
                        "short": False
                    },
                    {
                        "title": "表題",
                        "value": form.instance.title,
                        "short": False
                    },
                    {
                        "title": "本文",
                        "value": form.instance.body,
                        "short": False
                    },
                    {
                        "title": "送信者",
                        "value": str(form.instance.writer),
                        "short": False
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "name": "response",
                        "text": "対応する",
                        "url": settings.BASE_URL + str(reverse_lazy(
                            'home:contact_detail',
                            kwargs={'pk': self.object.pk}
                        )),
                        "style": "primary"
                    }
                ],
            }]
            slack_message(
                'home/slack/contact_received.slack', context, attachments
            )

        # お問い合わせを行った本人にメールを送信する
        subject = 'お問い合わせ受理: %s' % form.instance.title
        context = {
            'contact': form.instance,
        }
        from_email = settings.EMAIL_HOST_USER
        message = render_to_string(
            'home/mails/contact_received.txt', context
        )
        recipient_list = [form.instance.writer.email]
        send_mail(subject, message, from_email, recipient_list)

        # message 発出
        messages.success(
            self.request, 'お問い合わせを受理しました！'
        )

        return super().form_valid(form)


def get_contact_kind_accesible_pk_list(self):
    """管轄内のお問い合わせ種別の pk リストを取得

    ログインしている User が所属している Group を管轄に含む
    ContactKind の pk を取得
    """

    return self.request.user.groups.values_list(
        'officegroup__contactkind', flat=True
    )


class ContactKindView(mixins.StaffOnlyMixin, generic.TemplateView):
    """お問い合わせ種別一覧画面

    お問い合わせの種別と管轄を表示
    スタッフ専用
    """

    template_name = 'home/contact_kind.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ContactKind を全件取得
        context['contact_kind_list'] = ContactKind.objects.all()

        # ログインしている User が所属している Group を管轄に含む
        # ContactKind の pk を取得
        # （i.e. 管轄内のお問い合わせ種別の pk リストを取得）
        context['contact_kind_accesible_pk_list'] = \
            get_contact_kind_accesible_pk_list(self)

        return context


class ContactListView(mixins.StaffOnlyMixin, generic.TemplateView):
    """お問い合わせ一覧画面

    url で指定した pk の ContactKind に該当する Contact を一覧表示
    お問い合わせ管轄内のスタッフ専用
    """

    template_name = 'home/contact_list.html'

    def get(self, request, **kwargs):
        # 管轄外のスタッフのアクセスを阻止
        if int(self.kwargs['pk']) \
                not in get_contact_kind_accesible_pk_list(self):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contact_kind'] = ContactKind.objects.get(pk=self.kwargs['pk'])
        context['contact_list'] = Contact.objects.filter(
            kind__pk=self.kwargs['pk']
        ).order_by(
            '-create_datetime'
        )

        return context


class ContactDetailView(mixins.StaffOnlyMixin, generic.TemplateView):
    """お問い合わせ詳細画面

    pk は Contact の pk
    """

    template_name = 'home/contact_detail.html'

    def get(self, request, **kwargs):
        # 管轄外のスタッフのアクセスを阻止
        contact = Contact.objects.get(pk=self.kwargs['pk'])

        if contact.kind.pk \
                not in get_contact_kind_accesible_pk_list(self):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contact'] = Contact.objects.get(pk=self.kwargs['pk'])
        return context
