from django.views import generic

from datetime import datetime
from penguin.mixins import StaffOnlyMixin
from period import models
from period.functions import is_active


class ListView(StaffOnlyMixin, generic.TemplateView):
    """Period 系モデルの一覧や状態を表示

    スタッフのみアクセスできるが、変更ができるのはシステム管理者のみ
    """
    template_name = 'period/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ListView に表示したい Period 系モデルを列挙
        period_list = [
            models.PeriodThemeSubmit,
            models.PeriodThemeFirstVote,
            models.PeriodThemeFinalVote
        ]

        # 現在時刻を登録
        context['now'] = datetime.now()

        # context に情報を登録する
        context['object_list'] = [
            {
                'name': period._meta.verbose_name,
                'list': period.objects.all(),
                'active': is_active(period)
            } for period in period_list
        ]

        return context
