import csv
import io

from django.contrib.auth.models import Group
from django.db.models import Max

from home.models import ContactKind, GroupInfo, User
from home.views.helper_staff_member import get_staff_member_list


def success_group(csvfile):
    # invalid_group_list は不要なので捨てる
    valid_group_dict, _ = csv_group_to_dict(csvfile)

    # 今回作成した Group の pk を保管する
    created_group_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for group_name, information in valid_group_dict.items():
        group = Group.objects.create(name=group_name)
        group.save()
        created_group_pk_list.append(group.pk)
        group_info = GroupInfo.objects.create(
            group=group,
            email=information['email'],
            slack_ch=information['slack_ch']
        )
        group_info.save()

    # order = 0 (default) をもつ GroupInfo に対して order を割り当てる
    # ※order は admin サイトなどで表示される順序
    max_order = \
        GroupInfo.objects.all().aggregate(Max('order'))['order__max']
    counter = 1
    for unordered_group_info in GroupInfo.objects.filter(order=0):
        unordered_group_info.order = max_order + counter
        unordered_group_info.save()
        counter = counter + 1

    # 完了画面描画用の context
    return {
        'group_list': Group.objects.all(),
        'created_group_pk_list': created_group_pk_list
    }


def success_contact_kind(csvfile):
    # 情報を取得
    contact_kind_dict = csv_contact_kind_to_dict(csvfile)

    # 今回作成した ContactKind の pk を保管する
    created_contact_kind_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for contact_kind_name, group_list in contact_kind_dict.items():
        # Save!
        contact_kind = ContactKind.objects.create(name=contact_kind_name)
        contact_kind.groups.add(*group_list)
        contact_kind.save()

        # 作成したリストに pk を保管
        created_contact_kind_pk_list.append(contact_kind.pk)

    # order = 0 (default) をもつ GroupInfo に対して order を割り当てる
    # ※order は admin サイトなどで表示される順序
    max_order = \
        ContactKind.objects.all().aggregate(Max('order'))['order__max']
    counter = 1
    for unordered_contact_kind_info in ContactKind.objects.filter(order=0):
        unordered_contact_kind_info.order = max_order + counter
        unordered_contact_kind_info.save()
        counter = counter + 1

    return {
        'contact_kind_list': ContactKind.objects.all(),
        'created_contact_kind_pk_list': created_contact_kind_pk_list
    }


def success_staff_register(csvfile):
    # 情報を取得
    staff_register_dict, _ = csv_staff_register_to_dict(csvfile)

    # 今回作成した StaffRegister の pk を保管する
    created_staff_register_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for _, value in staff_register_dict.items():
        user = value['user']
        user.is_staff = True
        user.groups.clear()
        user.groups.add(*value['group_list'])
        user.save()

        # 作成したリストに pk を保管
        created_staff_register_pk_list.append(user.pk)

    return {
        'object_list': get_staff_member_list(),
        'created_staff_register_pk_list':
        created_staff_register_pk_list
    }


def csv_group_to_dict(csvfile):
    """[CSV] group.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        list: 登録される Group, GroupInfo に関する情報
        list: 登録できない Group, GroupInfo に関する情報（重複データ）
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # header 行を pass
    next(reader)

    # dict 初期化
    valid_group_dict = {}
    invalid_group_dict = {}

    # 1 行ずつデータを取り出し
    for row in reader:
        group_name = row[0]
        groupinfo_email = row[1]
        groupinfo_slack_ch = row[2]

        if Group.objects.filter(name=group_name).exists():
            # すでに作成された Group の場合は無効
            invalid_group_dict[group_name] = {
                'email': groupinfo_email,
                'slack_ch': groupinfo_slack_ch
            }
        else:
            # そうでなければ有効
            valid_group_dict[group_name] = {
                'email': groupinfo_email,
                'slack_ch': groupinfo_slack_ch
            }

    return valid_group_dict, invalid_group_dict


def csv_contact_kind_to_dict(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: ContactKind についての情報
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # 初期化
    contact_kind_dict = {}

    # header 行を pass
    next(reader)

    # 1 行ずつデータを取り出し
    for row in reader:
        contact_name = row[0]
        group_list = [
            Group.objects.get(groupinfo__order=i)
            for i, data in enumerate(row) if data == '1'
        ]

        # 管轄となる Group を取得
        contact_kind_dict[contact_name] = group_list

    return contact_kind_dict


def csv_staff_register_to_dict(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: 有効
        list: 無効（該当ユーザーなし）
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # header 行を pass
    next(reader)

    # User が存在するかどうかで振り分け
    valid_username_dict = {}
    invalid_username_list = []

    # 1 行ずつデータを取り出し
    for row in reader:
        username = row[0]
        if User.objects.filter(username=username).exists():
            group_list = [
                Group.objects.get(groupinfo__order=i)
                for i, data in enumerate(row) if data == '1'
            ]
            valid_username_dict[username] = {
                'user': User.objects.get(username=username),
                'group_list': group_list
            }
        else:
            invalid_username_list.append(username)

    return valid_username_dict, invalid_username_list
