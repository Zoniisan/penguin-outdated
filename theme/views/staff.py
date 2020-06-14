import csv
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import mixins
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

from penguin.forms import PeriodForm
from penguin.functions import period_active
from theme import forms, models


class PeriodView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """統一テーマ案募集・予選投票期間・決選投票期間を表示

    各期間の有効・無効を判定し表示
    """
    template_name = 'theme/period.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 現在時刻を取得
        now = datetime.now()
        context['now'] = now

        # 各 Period を全件取得
        context['app_list'] = models.PeriodApplication.objects.all()
        context['first_list'] = models.PeriodFirstVote.objects.all()
        context['final_list'] = models.PeriodFinalVote.objects.all()

        # 有効期間内かどうかを調べる
        context['app_active'] = period_active(models.PeriodApplication)
        context['first_active'] = period_active(models.PeriodFirstVote)
        context['final_active'] = period_active(models.PeriodFinalVote)

        return context


class PeriodCreateView(mixins.PermissionRequiredMixin, generic.FormView):
    """統一テーマ案募集・予選投票期間・決選投票期間を表示

    各期間の有効・無効を判定し表示
    """
    template_name = 'theme/period_create.html'
    permission_required = 'theme.view_theme'
    form_class = PeriodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # mode を日本語に直して context に登録
        context['mode_verbose'] = \
            mode_to_period_information(self.kwargs['mode'])['verbose_name']

        return context

    def form_valid(self, form):
        # mode をを取得
        mode = self.kwargs['mode']

        # mode に応じて情報を取得
        period_information = mode_to_period_information(mode)

        # save!
        obj = period_information['period'].objects.create(
            **form.cleaned_data
        )
        obj.save()

        # message 発行
        messages.success(
            self.request, '%s期間を登録しました！' %
            mode_to_period_information(mode)['verbose_name']
        )

        return redirect('theme:period')


def period_delete(self, mode, pk):
    """指定した Period を削除する
    """
    # delete
    mode_to_period_information(mode)['period'].objects.get(
        pk=pk
    ).delete()

    # message 発行
    messages.error(
        self, '%s期間を削除しました！' %
        mode_to_period_information(mode)['verbose_name']
    )

    return redirect('theme:period')


def mode_to_period_information(mode):
    """指定した mode を日本語とモデルオブジェクトに直す

    Ex. application → 統一テーマ応募
    """
    verbose_dict = {
        'application': {
            'verbose_name': '統一テーマ応募',
            'period': models.PeriodApplication,
        },
        'first_vote': {
            'verbose_name': '予選投票',
            'period': models.PeriodFirstVote,
        },
        'final_vote': {
            'verbose_name': '決勝投票',
            'period': models.PeriodFinalVote,
        },
    }

    return verbose_dict[mode]


class ListView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """統一テーマ案一覧・受理画面

    統一テーマ案の一覧を表示し、受理・詳細表示が可能
    """
    template_name = 'theme/list.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧
        context['theme_list'] = models.Theme.objects.all()

        return context


class DetailView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """統一テーマ案詳細

    統一テーマ案の詳細、応募者の情報を表示
    """
    template_name = 'theme/detail.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧
        context['theme'] = models.Theme.objects.get(pk=self.kwargs['pk'])

        return context


def accept(self, pk):
    """統一テーマ案を受理する
    """
    # アクセスは統一テーマ案担当のみ
    if not self.user.has_perm('theme.view_theme'):
        raise PermissionError

    # pk で指定した統一テーマ案に仮の予選コードを与える
    theme = models.Theme.objects.get(pk=pk)
    theme.first_id = 'TA'
    theme.save()

    # 予選コードの振り直し
    apply_first_id()

    # message 登録
    messages.success(self, '受理しました')

    return redirect('theme:list')


def disaccept(self, pk):
    """統一テーマ案を受理取り消しする
    """
    # アクセスは統一テーマ案担当のみ
    if not self.user.has_perm('theme.view_theme'):
        raise PermissionError

    # pk で指定した統一テーマ案から予選コードを剥奪する
    theme = models.Theme.objects.get(pk=pk)
    theme.first_id = None
    theme.save()

    # 予選コードの振り直し
    apply_first_id()

    # message 登録
    messages.error(self, '受理を取り消しました')

    return redirect('theme:list')


def apply_first_id():
    """予選コードを振り直す
    """
    first_accept_theme_list = [
        obj for obj in models.Theme.objects.all() if obj.first_accepted()
    ]

    # 予選コードを振り直す
    for count, first_accept_theme in enumerate(first_accept_theme_list):
        first_accept_theme.first_id = "TA-%s" % str(count + 1).zfill(3)
        first_accept_theme.save()


def csv_download(self):
    """CSV ファイルダウンロード

    統一テーマ案の CSV ファイルをダウンロードする。
    CSV ファイルはこの場で作成し、ファイルはサーバーに残さない。
    """
    # アクセスは統一テーマ案担当のみ
    if not self.user.has_perm('theme.view_theme'):
        raise PermissionError

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="theme.csv"'

    # CSV 書き出し
    writer = csv.writer(response)

    # ヘッダー行
    writer.writerow(['統一テーマ案', '趣意文'])

    # 各データ行
    for theme in models.Theme.objects.all():
        writer.writerow([theme.theme, theme.description])

    # response を返す
    return response


class FirstVoteResultView(mixins.PermissionRequiredMixin, generic.FormView):
    """予選投票結果画面

    予選投票の結果を表示し、決選投票の候補を確定する
    """
    template_name = 'theme/first_vote_result.html'
    permission_required = 'theme.view_theme'
    form_class = forms.FinishVoteCountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧（予選獲得票数順）
        context['theme_list'] = models.Theme.objects.filter(
            first_id__isnull=False
        ).annotate(first_count=Count('firstvote')).order_by('-first_count')

        return context

    def form_valid(self, form):
        # form で指定した上位 n 件を取得
        final_theme_set = models.Theme.objects.filter(
            first_id__isnull=False
        ).annotate(
            first_count=Count('firstvote')
        ).order_by('-first_count')[:form.cleaned_data['count']]

        # 決選コードを一旦全削除
        for theme in models.Theme.objects.all():
            theme.final_id = None
            theme.save()

        # 決選コードを割り当てる
        for rank, final_theme in enumerate(final_theme_set):
            final_theme.final_id = "TB-%s" % str(rank + 1).zfill(3)
            final_theme.save()

        # message 登録
        messages.success(self.request, '決選コードを割り当てました！')

        return redirect('theme:first_vote_result')
