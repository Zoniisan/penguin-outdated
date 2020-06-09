from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from home import forms
from home.models import Contact, Notification, NotificationRead, User
from home.tasks import send_mail_async
from penguin import mixins
from penguin.functions import set_paging_parameter


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

        context = {
            'notification': self.object,
            'base_url': settings.BASE_URL,
        }

        for user in self.object.to.all():
            # body を描画
            context['user'] = user
            body = render_to_string(
                'home/mails/notification.txt', context
            )

            # メールを送信
            send_mail_async.delay(
                subject,
                body,
                [user.email],
                reply_to=[self.object.group.groupinfo.email]
            )

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
