from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from home.models import Notice
from penguin import mixins


class NoticeView(mixins.AdminOnlyMixin, generic.CreateView):
    """お知らせ管理画面

    システム管理者のみ利用可能
    """

    template_name = 'home/notice.html'
    fields = ('title', 'body')
    model = Notice
    success_url = reverse_lazy('home:notice')

    def form_valid(self, form):
        # writer を登録
        form.instance.writer = self.request.user

        # message 発出
        messages.success(
            self.request, 'お知らせ「%s」を登録しました！' %
            form.instance.title
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice_list'] = Notice.objects.all()
        return context


def notice_delete(self, pk):
    """お知らせを削除

    システム管理者のみ利用可能
    """
    # admin only
    if not self.user.is_superuser:
        raise PermissionDenied

    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.error(self, 'お知らせ「%s」を削除しました！' % notice.title)
    return redirect('home:notice')


class NoticeUpdateView(mixins.AdminOnlyMixin, generic.UpdateView):
    """お知らせ更新画面

    システム管理者のみ利用可能
    """

    template_name = 'home/notice_update.html'
    fields = ('title', 'body')
    model = Notice
    success_url = reverse_lazy('home:notice')

    def form_valid(self, form):
        # writer を登録
        form.instance.writer = self.request.user

        # message 発出
        messages.success(
            self.request, 'お知らせ「%s」を更新しました！' %
            form.instance.title
        )

        return super().form_valid(form)
