import csv

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import generic

from home import forms
from home.views import helper_csv
from penguin import mixins


class CsvView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 フォーム画面

    CSV ファイルのダウンロードとアップロードを行う。
    mode に応じたテンプレートを返すだけ。
    """

    form_class = forms.CsvForm

    def get_template_names(self):
        """template_name の代用

        リストで返す必要があるので注意
        """
        return ['home/csv_%s.html' % self.kwargs['mode']]


class CsvConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 確認画面

    アップロードした CSV ファイルを読み込み、
    処理結果のプレビューを表示する。
    """
    form_class = forms.CsvForm

    def form_valid(self, form):
        # mode, csvfile を取得
        mode = self.kwargs['mode']
        csvfile = form.cleaned_data['csvfile']

        # context は確認画面の描画に必要。form をあらかじめ登録しておく。
        context = {'form': form}

        # mode ごとに必要な情報を取り出す
        if mode == 'group':
            context['valid_group_dict'], context['invalid_group_dict'] = \
                helper_csv.csv_to_object_group(csvfile)
        elif mode == 'contact_kind':
            context['contact_kind_dict'] = \
                helper_csv.csv_to_object_contact_kind(csvfile)
        elif mode == 'staff_register':
            context['valid_user_dict'], context['invalid_user_list'] = \
                helper_csv.csv_to_object_staff_register(csvfile)
        else:
            # 通常ここには到達しないはず
            raise Http404

        # 画面描画
        return render(self.request, 'home/csv_%s_confirm.html' % mode, context)

    def form_invalid(self, form):
        # ファイルに不備があった場合
        return helper_csv.file_invalid(self.request, self.kwargs['mode'])


class CsvSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """CSV 処理 完了画面

    実際に処理を行い、処理結果を表示する。
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        # mode, csvfile を取得する
        mode = self.kwargs['mode']
        csvfile = form.cleaned_data['csvfile']

        # mode に応じて実際の処理を行う
        if mode == 'group':
            context = helper_csv.success_group(csvfile)
        elif mode == 'contact_kind':
            context = helper_csv.success_contact_kind(csvfile)
        elif mode == 'staff_register':
            context = helper_csv.success_staff_register(csvfile)
        else:
            # 通常ここには到達しないはず
            raise Http404

        # 画面描画
        return render(self.request, 'home/csv_%s_success.html' % mode, context)

    def form_invalid(self, form):
        # ファイルに不備があった場合
        return helper_csv.file_invalid(self.request, self.kwargs['mode'])


def csv_download(request, mode):
    """CSV テンプレートファイルダウンロード

    CSV 処理に用いるテンプレートファイルをダウンロードさせる。
    CSV ファイルはこの場で作成し、ファイルはサーバーに残さない。
    """
    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="%s.csv"' % mode

    # CSV 書き出し
    writer = csv.writer(response)

    # mode に応じてヘッダー行を描画
    if mode == 'group':
        writer.writerow([
            'Group.name（例：総合対応局 システム担当）',
            'GroupInfo.email（例：system@example.com）',
            'GroupInfo.slack_ch（例：st-system）'
        ])
    elif mode == 'contact_kind':
        # 部局担当リスト（管轄する部局の欄に 1 を入力する）
        # データ書き出し
        writer.writerow(
            ['ContactKind.name（例：11 月祭全般についてのお問い合わせ）']
            + helper_csv.get_group_list()
        )
    elif mode == 'staff_register':
        # データ書き出し
        writer.writerow(
            ['User.username（例：1029290000）'] + helper_csv.get_group_list()
        )
    else:
        # 通常ここには到達しない
        raise Http404

    # response を返す
    return response
