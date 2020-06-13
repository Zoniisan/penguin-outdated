from django.conf import settings
from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django_slack import slack_message

from home.tasks import send_mail_async
from penguin.functions import period_active
from theme import forms, models


class ApplicationView(mixins.LoginRequiredMixin, generic.FormView):
    """統一テーマ案の応募を行う
    """
    template_name = 'theme/application.html'
    form_class = forms.ThemeForm
    success_url = reverse_lazy('home:index')

    def get(self, request, **kwargs):
        # 有効期限外の場合は 403
        if not period_active(models.PeriodApplication):
            raise PermissionDenied

        # 個人情報を入力していない = E メールを登録してないユーザーは先に
        # 個人情報を入力してもらう
        if not request.user.email:
            messages.error(request, '先に個人情報を入力してください。')
            return redirect('home:signup_token')

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 既に応募済みの統一テーマが存在する場合はフォームを無効化し
        # その内容を表示する。存在しない場合は None が格納される
        context['applied_theme'] = models.Theme.objects.filter(
            writer=self.request.user
        ).first()

        return context

    def form_valid(self, form):
        # 統一テーマを保存する
        obj = models.Theme.objects.create(
            writer=self.request.user,
            **form.cleaned_data
        )
        obj.save()

        # 統一テーマの管轄部局に slack を送る
        context = {
            'theme': obj,
        }
        attachments = [{
            "fallback": "統一テーマ受理",
            "color": "#2ed0d9",
            "fields": [
                {
                    "title": "統一テーマ",
                    "value": obj.theme,
                    "short": False
                },
                {
                    "title": "趣意文",
                    "value": obj.description,
                    "short": False
                },
                {
                    "title": "応募者",
                    "value": str(obj.writer),
                    "short": False
                }
            ],
            "actions": [
                {
                    "type": "button",
                    "name": "response",
                    "text": "詳細を確認する",
                    "url": settings.BASE_URL + str(reverse_lazy(
                        'home:contact_detail',
                        kwargs={'pk': obj.pk}
                    )),
                    "style": "primary"
                }
            ],
        }]
        # 統一テーマの管轄部局
        # = theme.view_theme の Permission をもつ Group
        for group in Group.objects.filter(permissions__name='Can view 統一テーマ案'):
            context['group'] = group
            slack_message(
                'theme/slack/theme_received.slack', context, attachments
            )

        # 応募者に E メールを送信
        subject = '統一テーマ案受付: %s' % obj.theme
        context = {
            'theme': obj,
        }
        body = render_to_string(
            'theme/mails/theme_received.txt', context
        )
        to_list = [obj.writer.email]
        send_mail_async.delay(
            subject,
            body,
            to_list
        )

        # message を登録する
        messages.success(
            self.request, '統一テーマの応募を受け付けました！'
        )

        return super().form_valid(form)
