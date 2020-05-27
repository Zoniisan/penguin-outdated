from django import template
import re

register = template.Library()


@register.inclusion_tag('pagination.html', takes_context=True)
def pagination(context):
    """
    ページングコントローラを表示
    """

    # ページに当たる部分は url から削除
    url = re.sub(
        '/p=[0-9]+', '',
        context['request'].path
    )

    return {
        'page_object': context['page_object'],
        'page_no': context['page_no'],
        'page_range': context['page_range'],
        'url': url,
    }
