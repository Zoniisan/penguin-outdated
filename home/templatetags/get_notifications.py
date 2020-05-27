from django import template
from home.models import Notification

register = template.Library()


@register.tag()
def get_notifications(parser, token):
    """GetNotifications を呼び出すだけ
    """
    return GetNotifications()


class GetNotifications(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        # 与えられた user 宛の通知をすべて取り出す
        context['all_notification_list'] = Notification.objects.filter(
            to=context['user']
        ).order_by('-create_datetime')[:5]
        # 既読の通知をすべて取り出す
        context['read_notification_list'] = [
            n for n in Notification.objects.all() if n.has_read(context['user'])
        ]
        # 未読件数を調べる
        context['unread_count'] = Notification.objects.filter(
            to=context['user']
        ).count() - len(context['read_notification_list'])

        return ''
