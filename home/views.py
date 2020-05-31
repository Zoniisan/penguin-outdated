import csv
import io
import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core import mail
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django_slack import slack_message

from home import forms
from home.models import (Contact, ContactKind, GroupInfo, Notice, Notification,
                         NotificationRead, User, UserToken)
from penguin import mixins
from penguin.functions import set_paging_parameter


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
        for group in form.instance.kind.groups.all():
            context = {
                'group': group,
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
        'contactkind', flat=True
    ).distinct()


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
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        if contact.kind.pk \
                not in get_contact_kind_accesible_pk_list(self):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contact'] = Contact.objects.get(pk=self.kwargs['pk'])
        return context


class NotificationView(mixins.StaffOnlyMixin, generic.CreateView):
    """通知システム

    スタッフのみ
    """

    template_name = 'home/notification.html'
    form_class = forms.NotificationForm
    model = Notification
    success_url = reverse_lazy('home:notification')

    def get(self, request, **kwargs):
        # 全員送信はスーパーユーザーの専権事項
        # （この仕様については要検討）
        if self.kwargs['mode'] == 'all' and not self.request.user.is_superuser:
            raise PermissionDenied

        return super().get(request, **kwargs)

    def form_valid(self, form):
        # sender を登録
        form.instance.sender = self.request.user

        # save
        self.object = form.save()

        # 宛先にメールを送信する
        subject = '通知: %s' % form.instance.title

        from_email = settings.EMAIL_HOST_USER

        context = {
            'object': self.object,
            'base_url': settings.BASE_URL,
        }

        # 同一コネクションで 1 人 1 件ずつ送信
        # Todo: 非同期送信の実装
        with mail.get_connection() as connection:
            for user in self.object.to.all():
                context['user'] = user
                message = render_to_string(
                    'home/mails/notification.txt', context
                )
                mail.EmailMessage(
                    subject,
                    message,
                    from_email,
                    [user.email],
                    connection=connection
                ).send()

        # message 発出
        messages.success(
            self.request, '通知を送信しました！'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 送信モード
        context['mode'] = self.kwargs['mode']

        # 新規作成する場合は自分の担当のみ選択可能
        context['form'].fields['group'].queryset = \
            self.request.user.groups.all()

        if self.kwargs['mode'] == 'reply_to_contact':
            # Contact に対する返信
            contact = Contact.objects.get(pk=self.kwargs['contact_pk'])
            context['form'].fields['to'].initial = [contact.writer]
            context['form'].fields['title'].initial = \
                "お問い合わせ「%s」について" % contact.title
            body_context = {
                'contact': contact
            }
            context['form'].fields['body'].initial = render_to_string(
                'home/others/notification_reply_to_contact.txt', body_context
            )
        elif self.kwargs['mode'] == 'all':
            # 全員送信
            context['form'].fields['to'].initial = User.objects.all()

        return context


def get_notification_accesible_pk_list(self):
    """管轄内の通知の pk リストを取得

    ログインしている User が所属している Group を担当に指定した
    Notification の pk を取得
    """

    return self.request.user.groups.values_list(
        'notification', flat=True
    ).distinct()


class NotificationStaffListView(mixins.StaffOnlyMixin, generic.TemplateView):
    """通知一覧画面（スタッフ向け）

    自分の担当が送信した通知以外は閲覧できない
    """

    template_name = 'home/notification_staff_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notification_list = Notification.objects.filter(
            pk__in=get_notification_accesible_pk_list(self)
        ).order_by('-create_datetime')

        # ページング処理
        set_paging_parameter(self.kwargs, context, notification_list)
        return context


class NotificationStaffDetailView(mixins.StaffOnlyMixin, generic.TemplateView):
    """通知詳細画面（スタッフ向け）

    自分の担当が送信した通知以外は閲覧できない
    """

    template_name = 'home/notification_staff_detail.html'

    def get(self, request, **kwargs):
        if int(self.kwargs['pk']) not in \
                get_notification_accesible_pk_list(self):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 通知
        notification = Notification.objects.get(
            pk=self.kwargs['pk']
        )
        context['notification'] = notification

        # 既読リスト
        to_list = list()
        for user in notification.to.all():
            try:
                notification_read = NotificationRead.objects.get(
                    notification=notification,
                    user=user
                )
                to_list.append({
                    'user': user,
                    'read': notification_read
                })
            except NotificationRead.DoesNotExist:
                to_list.append({
                    'user': user,
                    'read': None
                })

        context['to_list'] = to_list

        return context


class NotificationListView(LoginRequiredMixin, generic.TemplateView):
    """通知一覧画面

    自分宛ての通知のみ閲覧できる
    """

    template_name = 'home/notification_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 自分宛ての通知のリスト
        notification_list = Notification.objects.filter(
            to=self.request.user
        ).order_by('-create_datetime')

        # 自分宛ての通知とその既読状況の辞書を投げる
        obj_list = [
            {
                'notification': n,
                'read': n.has_read(self.request.user)
            } for n in notification_list
        ]

        # ページング処理
        set_paging_parameter(self.kwargs, context, obj_list)
        return context


class NotificationDetailView(LoginRequiredMixin, generic.TemplateView):
    """通知詳細画面

    自分の受信した通知以外は閲覧できない
    """

    template_name = 'home/notification_detail.html'

    def get(self, request, **kwargs):
        # 自分が受信した通知以外は閲覧できない
        notification = get_object_or_404(Notification, pk=self.kwargs['pk'])
        if self.request.user not in notification.to.all():
            raise PermissionDenied

        # 初閲覧の場合は既読記録を残す
        read, created = NotificationRead.objects.get_or_create(
            user=self.request.user, notification=notification
        )
        read.save()

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 通知
        notification = get_object_or_404(Notification, pk=self.kwargs['pk'])
        context['notification'] = notification

        return context


class StaffListView(mixins.StaffOnlyMixin, generic.TemplateView):
    """事務局員名簿

    スタッフ専用
    """

    template_name = 'home/staff_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 事務局員名簿を作成
        # 部局担当別、学年・氏名読みがな順でリストを作成
        context['object_list'] = [
            {
                'group': group,
                'member_list': group.user_set.all().order_by(
                    '-grade', 'last_name_kana', 'first_name_kana'
                )
            }
            for group in Group.objects.all().order_by('groupinfo__order')
        ]

        return context


def download_staff_vcards(request, mode):
    """事務局員の連絡先を vcard 形式でダウンロード

    スタッフ専用
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


class CsvGroupView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    フォーム画面
    """

    template_name = 'home/csv_group.html'
    form_class = forms.CsvForm


class CsvGroupConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 登録できる情報とできない情報に振り分ける
        valid_group_dict, invalid_group_dict = csv_group_to_dict(csvfile)

        return render(
            self.request, 'home/csv_group_confirm.html', {
                'form': form,
                'valid_group_dict': valid_group_dict,
                'invalid_group_dict': invalid_group_dict
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_group')


class CsvGroupSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # invalid_group_list は不要なので捨てる
        valid_group_dict, _ = csv_group_to_dict(csvfile)

        # 今回作成した Group の pk を保管する
        created_group_pk_list = []

        # valid_group_dict の内容に基づいてモデルを作成する
        for group_name, information in valid_group_dict.items():
            group = Group.objects.create(name=group_name)
            group.save()
            created_group_pk_list.append(group.pk)
            group_info = GroupInfo.objects.create(
                group=group,
                email=information['email'],
                slack_ch=information['slack_ch']
            )
            group_info.save()

        # order = 0 (default) をもつ GroupInfo に対して order を割り当てる
        # ※order は admin サイトなどで表示される順序
        max_order = \
            GroupInfo.objects.all().aggregate(Max('order'))['order__max']
        counter = 1
        for unordered_group_info in GroupInfo.objects.filter(order=0):
            unordered_group_info.order = max_order + counter
            unordered_group_info.save()
            counter = counter + 1

        return render(
            self.request, 'home/csv_group_success.html', {
                'group_list': Group.objects.all(),
                'created_group_pk_list': created_group_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_group')


def csv_group_to_dict(csvfile):
    """[CSV] group.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        list: 登録される Group, GroupInfo に関する情報
        list: 登録できない Group, GroupInfo に関する情報（重複データ）
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # header 行を pass
    next(reader)

    # dict 初期化
    valid_group_dict = {}
    invalid_group_dict = {}

    # 1 行ずつデータを取り出し
    for row in reader:
        group_name = row[0]
        groupinfo_email = row[1]
        groupinfo_slack_ch = row[2]

        if Group.objects.filter(name=group_name).exists():
            # すでに作成された Group の場合は無効
            invalid_group_dict[group_name] = {
                'email': groupinfo_email,
                'slack_ch': groupinfo_slack_ch
            }
        else:
            # そうでなければ有効
            valid_group_dict[group_name] = {
                'email': groupinfo_email,
                'slack_ch': groupinfo_slack_ch
            }

    return valid_group_dict, invalid_group_dict


def csv_group_download(request):
    """[CSV] Group, GroupInfo を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="group.csv"'

    # CSV 書き出し
    writer = csv.writer(response)
    writer.writerow([
        'Group.name（例：総合対応局 システム担当）',
        'GroupInfo.email（例：system@example.com）',
        'GroupInfo.slack_ch（例：st-system）'
    ])

    return response


class CsvContactKindView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    フォーム画面
    """

    template_name = 'home/csv_contact_kind.html'
    form_class = forms.CsvForm


class CsvContactKindConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        contact_kind_dict = csv_contact_kind_to_dict(csvfile)

        return render(
            self.request, 'home/csv_contact_kind_confirm.html', {
                'form': form,
                'contact_kind_dict': contact_kind_dict
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


class CsvContactKindSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        contact_kind_dict = csv_contact_kind_to_dict(csvfile)

        # 今回作成した ContactKind の pk を保管する
        created_contact_kind_pk_list = []

        # valid_group_dict の内容に基づいてモデルを作成する
        for contact_kind_name, group_list in contact_kind_dict.items():
            # Save!
            contact_kind = ContactKind.objects.create(name=contact_kind_name)
            contact_kind.groups.add(*group_list)
            contact_kind.save()

            # 作成したリストに pk を保管
            created_contact_kind_pk_list.append(contact_kind.pk)

        # order = 0 (default) をもつ GroupInfo に対して order を割り当てる
        # ※order は admin サイトなどで表示される順序
        max_order = \
            ContactKind.objects.all().aggregate(Max('order'))['order__max']
        counter = 1
        for unordered_contact_kind_info in ContactKind.objects.filter(order=0):
            unordered_contact_kind_info.order = max_order + counter
            unordered_contact_kind_info.save()
            counter = counter + 1

        return render(
            self.request, 'home/csv_contact_kind_success.html', {
                'contact_kind_list': ContactKind.objects.all(),
                'created_contact_kind_pk_list': created_contact_kind_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


def csv_contact_kind_to_dict(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: ContactKind についての情報
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # 初期化
    contact_kind_dict = {}

    # header 行を pass
    next(reader)

    # 1 行ずつデータを取り出し
    for row in reader:
        contact_name = row[0]
        group_list = [
            Group.objects.get(groupinfo__order=i)
            for i, data in enumerate(row) if data == '1'
        ]

        # 管轄となる Group を取得
        contact_kind_dict[contact_name] = group_list

    return contact_kind_dict


def csv_contact_kind_download(request):
    """[CSV] ContactKind を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="contact_kind.csv"'

    # CSV 書き出し
    writer = csv.writer(response)

    # 部局担当リスト（管轄する部局の欄に 1 を入力する）
    group_list = list(
        Group.objects.all().order_by(
            'groupinfo'
        ).values_list(
            'name', flat=True
        )
    )

    # データ書き出し
    writer.writerow(
        ['ContactKind.name（例：11 月祭全般についてのお問い合わせ）'] + group_list
    )

    return response


class CsvStaffRegisterView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Staff User を作成

    フォーム画面
    """

    template_name = 'home/csv_staff_register.html'
    form_class = forms.CsvForm


class CsvStaffRegisterConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Staff User を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        valid_user_dict, invalid_user_list \
            = csv_staff_register_to_dict(csvfile)

        return render(
            self.request, 'home/csv_staff_register_confirm.html', {
                'form': form,
                'valid_user_dict': valid_user_dict,
                'invalid_user_list': invalid_user_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


class CsvStaffRegisterSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] StaffRegister を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        staff_register_dict, _ = csv_staff_register_to_dict(csvfile)

        # 今回作成した StaffRegister の pk を保管する
        created_staff_register_pk_list = []

        # valid_group_dict の内容に基づいてモデルを作成する
        for _, value in staff_register_dict.items():
            user = value['user']
            user.is_staff = True
            user.groups.clear()
            user.groups.add(*value['group_list'])
            user.save()

            # 作成したリストに pk を保管
            created_staff_register_pk_list.append(user.pk)

        return render(
            self.request, 'home/csv_staff_register_success.html', {
                'object_list': [
                    {
                        'group': group,
                        'member_list': group.user_set.all().order_by(
                            '-grade', 'last_name_kana', 'first_name_kana'
                        )
                    }
                    for group in Group.objects.all().order_by(
                        'groupinfo__order'
                    )
                ],
                'created_staff_register_pk_list':
                    created_staff_register_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


def csv_staff_register_to_dict(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: 有効
        list: 無効（該当ユーザーなし）
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # header 行を pass
    next(reader)

    # User が存在するかどうかで振り分け
    valid_username_dict = {}
    invalid_username_list = []

    # 1 行ずつデータを取り出し
    for row in reader:
        username = row[0]
        if User.objects.filter(username=username).exists():
            group_list = [
                Group.objects.get(groupinfo__order=i)
                for i, data in enumerate(row) if data == '1'
            ]
            valid_username_dict[username] = {
                'user': User.objects.get(username=username),
                'group_list': group_list
            }
        else:
            invalid_username_list.append(username)

    return valid_username_dict, invalid_username_list


def csv_staff_register_download(request):
    """[CSV] StaffRegister を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="staff_register.csv"'

    # CSV 書き出し
    writer = csv.writer(response)

    # 部局担当リスト（管轄する部局の欄に 1 を入力する）
    group_list = list(
        Group.objects.all().order_by(
            'groupinfo'
        ).values_list(
            'name', flat=True
        )
    )

    # データ書き出し
    writer.writerow(
        ['User.username（例：1029290000）'] + group_list
    )

    return response
