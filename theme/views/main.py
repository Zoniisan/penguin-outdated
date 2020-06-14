from django.contrib import messages
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
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
