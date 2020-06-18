from django import template
from period.functions import get_period_object_list

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
        context['period_list'] = get_period_object_list()
        return ''
