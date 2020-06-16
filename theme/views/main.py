from django.conf import settings
from django.contrib import messages
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from period import models as period_models
from period.functions import is_active
from theme import forms, models


class SubmitView(mixins.LoginRequiredMixin, generic.FormView):
    """統一テーマ案応募
    """
    template_name = 'theme/submit.html'
    form_class = forms.SubmitForm
    success_url = reverse_lazy('theme:submit')

    def get(self, request, **kwargs):
        # 個人情報が登録されていない場合は登録を促す
        if not request.user.email:
            messages.error(request, 'まず個人情報を入力してください')
            return redirect('home:signup_token')

        # 期間外の場合は 403
        if not is_active(period_models.PeriodThemeSubmit):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 応募済みのデータ（なければ None)
        context['submitted_data'] = models.Theme.objects.filter(
            writer=self.request.user
        ).first()

        return context

    def form_valid(self, form):
        # すでに応募済みの場合は 403
        if models.Theme.objects.filter(writer=self.request.user).exists():
            raise PermissionDenied

        # 期間外の場合は 403
        if not is_active(period_models.PeriodThemeSubmit):
            raise PermissionDenied

        # インスタンスを作成
        theme = models.Theme.objects.create(
            writer=self.request.user,
            **form.cleaned_data
        )
        theme.save()

        # message を登録
        messages.success(self.request, '応募しました！')

        return super().form_valid(form)


class VoteView(mixins.LoginRequiredMixin, generic.TemplateView):
    """統一テーマ案投票
    """

    def get_template_names(self):
        """template_name の代用

        リストで返す必要があるので注意
        """
        return ['theme/%s_vote.html' % self.kwargs['mode']]

    def get(self, request, **kwargs):
        # model を取得
        model_dict = get_model_dict(self.kwargs['mode'])

        # 期間外の場合は 403
        if not is_active(model_dict['period']):
            raise PermissionDenied

        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # model を取得
        model_dict = get_model_dict(self.kwargs['mode'])

        # 統一テーマ一覧
        context['theme_list'] = model_dict['list']

        # 投票済みデータ
        context['voted'] = model_dict['eptid'].objects.filter(
            eptid=self.request.user.shib_eptid
        )

        # BASE_URL（ツイート用）
        context['base_url'] = settings.BASE_URL

        return context


def vote(request, mode, pk):
    """統一テーマ投票処理
    """
    # model を取得
    model_dict = get_model_dict(mode)

    # 期間外・投票済みの場合は 403
    if not is_active(model_dict['period']):
        raise PermissionDenied

    # すでに投票済みの場合は 403
    if model_dict['eptid'].objects.filter(
        eptid=request.user.shib_eptid
    ).exists():
        raise PermissionDenied

    # テーマを指定
    theme = get_object_or_404(models.Theme, pk=pk)

    # 投票データを登録
    obj = model_dict['vote'].objects.create(
        theme=theme
    )
    obj.save()
    obj_eptid = model_dict['eptid'].objects.create(
        eptid=request.user.shib_eptid
    )
    obj_eptid.save()

    # message を登録
    messages.success(request, '投票しました！')

    return redirect('theme:%s_vote' % mode)


def get_model_dict(mode):
    """mode(first/final) に応じてモデルを取得
    """
    if mode == 'first':
        return {
            'vote': models.FirstVote,
            'eptid': models.FirstVoteEptid,
            'period': period_models.PeriodThemeFirstVote,
            'list': models.Theme.objects.filter(first_id__isnull=False)
        }
    elif mode == 'final':
        return {
            'vote': models.FinalVote,
            'eptid': models.FinalVoteEptid,
            'period': period_models.PeriodThemeFinalVote,
            'list': models.Theme.objects.filter(final_id__isnull=False)
        }
