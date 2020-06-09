import csv

from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic

from home import forms
from home.views import helper_csv
from penguin import mixins


class CsvView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 フォーム画面
    """

    form_class = forms.CsvForm

    def get_template_names(self):
        """template_name の代用

        リストで返す必要があるので注意
        """
        return ['home/csv_%s.html' % self.kwargs['mode']]


class CsvConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 確認画面

    """
    form_class = forms.CsvForm

    def form_valid(self, form):
        mode = self.kwargs['mode']
        csvfile = form.cleaned_data['csvfile']

        # context は確認画面の描画に必要。form をあらかじめ登録しておく。
        context = {'form': form}

        # mode ごとに必要な情報を取り出す
        if mode == 'group':
            context['valid_group_dict'], context['invalid_group_dict'] = \
                helper_csv.csv_group_to_dict(csvfile)
        elif mode == 'contact_kind':
            context['contact_kind_dict'] = \
                helper_csv.csv_contact_kind_to_dict(csvfile)
        elif mode == 'staff_register':
            context['valid_user_dict'], context['invalid_user_list'] = \
                helper_csv.csv_staff_register_to_dict(csvfile)
        else:
            # 通常ここには到達しないはず
            raise Http404

        return render(self.request, 'home/csv_%s_confirm.html' % mode, context)

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_%s' % self.kwargs['mode'])


class CsvSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        mode = self.kwargs['mode']
        csvfile = form.cleaned_data['csvfile']

        if mode == 'group':
            context = helper_csv.success_group(csvfile)
        elif mode == 'contact_kind':
            context = helper_csv.success_contact_kind(csvfile)
        elif mode == 'staff_register':
            context = helper_csv.success_staff_register(csvfile)
        else:
            # 通常ここには到達しないはず
            raise Http404

        return render(self.request, 'home/csv_%s_success.html' % mode, context)

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_%s' % self.kwargs['mode'])


def csv_download(request, mode):
    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="%s.csv"' % mode

    # CSV 書き出し
    writer = csv.writer(response)

    if mode == 'group':
        writer.writerow([
            'Group.name（例：総合対応局 システム担当）',
            'GroupInfo.email（例：system@example.com）',
            'GroupInfo.slack_ch（例：st-system）'
        ])
    elif mode == 'contact_kind' or mode == 'staff_register':
        # 部局担当リスト（管轄する部局の欄に 1 を入力する）
        group_list = list(
            Group.objects.all().order_by(
                'groupinfo'
            ).values_list(
                'name', flat=True
            )
        )
        if mode == 'contact_kind':
            # データ書き出し
            writer.writerow(
                ['ContactKind.name（例：11 月祭全般についてのお問い合わせ）'] + group_list
            )
        elif mode == 'staff_register':
            # データ書き出し
            writer.writerow(
                ['User.username（例：1029290000）'] + group_list
            )
    else:
        # 通常ここには到達しない
        raise Http404

    return response
