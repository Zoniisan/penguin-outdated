from datetime import datetime


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
        finish__lte=now
    ).exists()
