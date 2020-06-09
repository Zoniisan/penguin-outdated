from django.contrib.auth.models import Group


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
