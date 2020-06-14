from datetime import datetime

from period import models


def is_active(period):
    """各期間が有効かどうかを返す

    Args:
        period(object): Period 系モデル

    Returns:
        bool: 有効なら True
    """
    # 現在時刻を取得
    now = datetime.now()

    # start <= now <= finish なるインスタンスがあれば True
    return period.objects.filter(
        start__lte=now,
        finish__gte=now
    ).exists()


def get_period_object_list():
    """period 系のモデルについて情報を返す
    """
    # Period 系モデルを列挙
    period_list = [
        {'period': models.PeriodThemeSubmit, 'url': 'theme:submit'},
        {'period': models.PeriodThemeFirstVote, 'url': 'theme:first_vote'},
        {'period': models.PeriodThemeFinalVote, 'url': 'home:index'}
    ]

    return [
        {
            'name': period['period']._meta.verbose_name,
            'omitted_name': period['period']._meta.verbose_name.rstrip('期間'),
            'list': period['period'].objects.all(),
            'active': is_active(period['period']),
            'url': period['url']
        } for period in period_list
    ]
