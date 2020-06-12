from datetime import datetime

from django.contrib import messages
from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.views import generic

from penguin.forms import PeriodForm
from penguin.functions import period_active
from theme import models


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
