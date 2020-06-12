import random
import string

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def get_staff_member_list():
    """ スタッフ名簿のリストを作成

    部局担当→スタッフ（学年・五十音順）の辞書リストを作成する
    """
    return [
        {
            'group': group,
            'member_list': group.user_set.all().order_by(
                '-grade', 'last_name_kana', 'first_name_kana'
            )
        }
        for group in Group.objects.all().order_by('groupinfo__order')
    ]


def pk_in_list_or_403(pk, pk_list):
    """pk が pk_list に入っていなければ 403 を返す
    """
    if pk not in pk_list:
        raise PermissionDenied


def craete_random_strings(count=100):
    """ランダム半角英数文字列を作成する

    文字数を指定しない場合は 100 文字とする
    """
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=count)
    )


def get_accesible_pk_list(user, model):
    """ある User がアクセスできるオブジェクトの pk を返す

    ContactKind, Notification に利用
    model はモデル名をすべて小文字にして文字列で与えること
    システム管理者はすべてのオブジェクトにアクセス可能とする
    """
    # システム管理者はすべての Group に所属するものとする
    group_list = Group.objects.all() if user.is_superuser else user.groups

    # 対応するオブジェクトの pk のリストを返す
    return group_list.values_list(model, flat=True).distinct()
