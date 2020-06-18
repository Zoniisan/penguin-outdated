from django.views import generic

from datetime import datetime
from penguin.mixins import StaffOnlyMixin
from period.functions import get_period_object_list


class ListView(StaffOnlyMixin, generic.TemplateView):
    """Period 系モデルの一覧や状態を表示

    スタッフのみアクセスできるが、変更ができるのはシステム管理者のみ
    """
    template_name = 'period/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 現在時刻を登録
        context['now'] = datetime.now()

        # context に情報を登録する
        context['object_list'] = get_period_object_list()

        return context
