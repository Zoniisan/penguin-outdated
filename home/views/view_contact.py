from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django_slack import slack_message

from home.models import Contact, ContactKind
from home.tasks import send_mail_async
from home.views.helper import get_accesible_pk_list, pk_in_list_or_403
from penguin import mixins


class ContactView(LoginRequiredMixin, generic.CreateView):
    """お問い合わせ作成画面

    Contact を作成するフォームを表示する。
    ついでに事務局の位置情報と電話番号も表示する。
    """

    template_name = 'home/contact.html'
    fields = ('kind', 'title', 'body')
    model = Contact
    success_url = reverse_lazy('home:contact')

    def form_valid(self, form):
        # writer を登録して Save する
        form.instance.writer = self.request.user
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
        body = render_to_string(
            'home/mails/contact_received.txt', context
        )
        to_list = [form.instance.writer.email]
        send_mail_async.delay(
            subject,
            body,
            to_list
        )

        # message を登録する
        messages.success(
            self.request, 'お問い合わせを受理しました！'
        )

        return super().form_valid(form)


class ContactKindView(mixins.StaffOnlyMixin, generic.TemplateView):
    """お問い合わせ種別一覧画面

    お問い合わせの種別と管轄を表示する。
    自分の担当に対応する種別のお問い合わせのみを選択できる。
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
            get_accesible_pk_list(self.request.user, 'contactkind')

        return context


class ContactListView(mixins.StaffOnlyMixin, generic.TemplateView):
    """お問い合わせ一覧画面

    url で指定した pk の ContactKind に該当する Contact を一覧表示
    お問い合わせ管轄内のスタッフ専用
    """

    template_name = 'home/contact_list.html'

    def get(self, request, **kwargs):
        # そもそも ContactKind が存在しない場合は 404
        contact_kind = get_object_or_404(ContactKind, pk=self.kwargs['pk'])

        # お問い合わせ管轄ではないスタッフのアクセスを拒否
        pk_in_list_or_403(
            contact_kind.pk,
            get_accesible_pk_list(self.request.user, 'contactkind')
        )

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # お問い合わせ種別
        context['contact_kind'] = ContactKind.objects.get(pk=self.kwargs['pk'])

        # お問い合わせ種別を指定した上でお問い合わせのリストを作成
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
        # そもそも Contact が存在しない場合は 404
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        # 管轄外のスタッフのアクセスを阻止
        pk_in_list_or_403(
            contact.kind.pk,
            get_accesible_pk_list(self.request.user, 'contactkind')
        )

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 詳細を表示する Contact
        context['contact'] = Contact.objects.get(pk=self.kwargs['pk'])
        return context
