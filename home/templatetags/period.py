from django import template

from penguin.functions import period_active
from theme.models import PeriodApplication, PeriodFinalVote, PeriodFirstVote

register = template.Library()


@register.tag()
def period(parser, token):
    """各 period が有効かどうかを調べて context に与える
    """
    return Period()


class Period(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        # 統一テーマ系
        context['theme_application_active'] = period_active(PeriodApplication)
        context['theme_first_vote_active'] = period_active(PeriodFirstVote)
        context['theme_final_vote_active'] = period_active(PeriodFinalVote)

        return ''
