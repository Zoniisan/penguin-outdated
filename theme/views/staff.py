import csv

from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from theme import forms, models


class ListView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """統一テーマ案一覧を表示し、受理するかどうかを選択させる
    """
    template_name = 'theme/staff_list.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧
        context['theme_list'] = models.Theme.objects.all()

        return context


class DetailView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """pk で指定した統一テーマ案の詳細を表示する
    """
    template_name = 'theme/staff_detail.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案
        context['theme'] = get_object_or_404(
            models.Theme, pk=self.kwargs['pk']
        )

        return context


@permission_required('theme.view_theme', raise_exception=True)
def accept(request, pk):
    """pk で指定した統一テーマ案を受理する
    """
    # テーマを指定
    theme = get_object_or_404(
        models.Theme, pk=pk
    )

    # 受理する統一テーマに仮の予選コードを与える
    theme.first_id = 'TA'
    theme.save()

    # 受理された統一テーマ案に予選コードを割り当てる
    apply_first_id()

    # message 登録
    messages.success(request, '受理しました')

    return redirect('theme:staff_list')


@permission_required('theme.view_theme', raise_exception=True)
def disaccept(request, pk):
    """pk で指定した統一テーマ案を受理取り消しする
    """
    # テーマを指定
    theme = get_object_or_404(
        models.Theme, pk=pk
    )

    # 受理取り消しする統一テーマ案の予選コードを剥奪
    theme.first_id = None
    theme.save()

    # 受理された統一テーマ案に予選コードを割り当てる
    apply_first_id()

    # message 登録
    messages.error(request, '受理取り消ししました')

    return redirect('theme:staff_list')


def apply_first_id():
    """受理された統一テーマ案に予選コードを割り当てる

    予選コードは応募順（受理順ではない）で形式は TA-000
    """
    # 受理された統一テーマ一覧
    theme_list = [
        obj for obj in models.Theme.objects.all() if obj.first_id
    ]

    # 予選コードを振り直す
    for count, theme in enumerate(theme_list):
        theme.first_id = "TA-%s" % str(count + 1).zfill(3)
        theme.save()


@permission_required('theme.view_theme', raise_exception=True)
def csv_download(self):
    """CSV ファイルダウンロード
    統一テーマ案の CSV ファイルをダウンロードする。
    """
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


class FirstVoteView(mixins.PermissionRequiredMixin, generic.FormView):
    """予選投票の結果を表示
    """
    template_name = 'theme/staff_first_vote.html'
    permission_required = 'theme.view_theme'
    form_class = forms.FinalAcceptForm
    success_url = reverse_lazy('theme:staff_first_vote')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧（予選票数順）
        context['theme_list'] = models.Theme.objects.filter(
            first_id__isnull=False
        ).annotate(first_count=Count('firstvote')).order_by('-first_count')

        return context

    def form_valid(self, form):
        # form で指定した上位 n 件を取得
        theme_list = models.Theme.objects.filter(
            first_id__isnull=False
        ).annotate(
            first_count=Count('firstvote')
        ).order_by('-first_count')[:form.cleaned_data['final_accept']]

        # 決選コードを一旦全削除
        for theme in models.Theme.objects.all():
            theme.final_id = None
            theme.save()

        # 決選コードを割り当てる
        for rank, final_theme in enumerate(theme_list):
            final_theme.final_id = "TB-%s" % str(rank + 1).zfill(3)
            final_theme.save()

        # message 登録
        messages.success(self.request, '決選コードを割り当てました')

        return super().form_valid(form)


class FinalVoteView(mixins.PermissionRequiredMixin, generic.TemplateView):
    """決選投票の結果を表示
    """
    template_name = 'theme/staff_final_vote.html'
    permission_required = 'theme.view_theme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 統一テーマ案一覧（予選票数順）
        context['theme_list'] = models.Theme.objects.filter(
            final_id__isnull=False
        ).annotate(final_count=Count('finalvote')).order_by('-final_count')

        return context
