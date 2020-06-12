import csv
import io

from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Max
from django.shortcuts import redirect

from home.models import ContactKind, GroupInfo, User
from home.views.helper import get_staff_member_list


def success_group(csvfile):
    """mode: group / 処理

    入力 csvfile に応じて Group, GroupInfo を作成する。
    返り値は処理結果画面の描画に用いる下の dict

    {
        'group_list': 全 Group の list
        'created_group_pk_list': 今回作成した Group の pk の list
    }
    """

    # invalid_group_list は不要なので捨てる
    valid_group_dict, _ = csv_to_object_group(csvfile)

    # 今回作成した Group の pk を保管する
    created_group_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for group_name, information in valid_group_dict.items():
        # Group を作成
        group = Group.objects.create(name=group_name)
        group.save()

        # 今回作成した Group の pk をリストに登録
        created_group_pk_list.append(group.pk)

        # GroupInfo を作成
        group_info = GroupInfo.objects.create(
            group=group,
            email=information['email'],
            slack_ch=information['slack_ch']
        )
        group_info.save()

    # order = 0 (default) をもつ GroupInfo に対して order を割り当てる
    # order は admin サイトなどで表示される順序
    attach_order(GroupInfo)

    # 完了画面描画用の context
    return {
        'group_list': Group.objects.all(),
        'created_group_pk_list': created_group_pk_list
    }


def success_contact_kind(csvfile):
    """mode: contact_kind / 処理

    入力 csvfile に応じて ContactKind を作成する。
    返り値は処理結果画面の描画に用いる下の dict

    {
        'contact_kind_list': 全 ContactKind の list,
        'created_contact_kind_pk_list': 今回作成した ContactKind の pk の list
    }
    """

    # 情報を取得
    contact_kind_dict = csv_to_object_contact_kind(csvfile)

    # 今回作成した ContactKind の pk を保管する
    created_contact_kind_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for contact_kind_name, group_list in contact_kind_dict.items():
        # ContactKind を作成
        contact_kind = ContactKind.objects.create(name=contact_kind_name)
        contact_kind.groups.add(*group_list)
        contact_kind.save()

        # 作成したリストに 今回作成した ContactKind の pk を保管
        created_contact_kind_pk_list.append(contact_kind.pk)

    # order = 0 (default) をもつ ContactKind に対して order を割り当てる
    # order は admin サイトなどで表示される順序
    attach_order(ContactKind)

    # 完了画面描画用の context
    return {
        'contact_kind_list': ContactKind.objects.all(),
        'created_contact_kind_pk_list': created_contact_kind_pk_list
    }


def success_staff_register(csvfile):
    """mode: staff_register / 処理

    入力 csvfile に応じて User を更新する。
    返り値は処理結果画面の描画に用いる下の dict

    {
        'object_list': スタッフ名簿, home.helper.get_staff_member_list 参照
        'created_staff_register_pk_list': 今回更新した User の list
    }
    """

    # 情報を取得
    staff_register_dict, _ = csv_to_object_staff_register(csvfile)

    # 今回更新した User の pk を保管する
    created_staff_register_pk_list = []

    # valid_group_dict の内容に基づいてモデルを作成する
    for _, value in staff_register_dict.items():
        # User を更新する
        user = value['user']
        user.is_staff = True
        user.groups.clear()
        user.groups.add(*value['group_list'])
        user.save()

        # 作成したリストに pk を保管
        created_staff_register_pk_list.append(user.pk)

    # 完了画面描画用の context
    return {
        'object_list': get_staff_member_list(),
        'created_staff_register_pk_list':
        created_staff_register_pk_list
    }


def csv_to_object_group(csvfile):
    """[CSV] group.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: 登録される Group, GroupInfo に関する情報
            Group.name →
                ('email' → GroupInfo.email, 'slack_ch' → GroupInfo.slack_ch)
        dict: 登録できない Group, GroupInfo に関する情報
            既に同じ Group.name の Group が存在する場合は登録できない
            Group.name →
                ('email' → GroupInfo.email, 'slack_ch' → GroupInfo.slack_ch)
    """
    # reader を取得
    reader = csvfile_to_reader(csvfile)

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


def csv_to_object_contact_kind(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: 登録する ContactKind に関する情報
            ContactKind.name → [ContactKind.group]
    """
    # reader を取得
    reader = csvfile_to_reader(csvfile)

    # 初期化
    contact_kind_dict = {}

    # header 行を pass
    next(reader)

    # 1 行ずつデータを取り出し
    for row in reader:
        contact_kind_name = row[0]
        group_list = get_group_list(row)

        # 管轄となる Group を取得
        contact_kind_dict[contact_kind_name] = group_list

    return contact_kind_dict


def csv_to_object_staff_register(csvfile):
    """[CSV] contact_kind.csv から list を作成する

    Args:
        csvFile(file): CSV ファイル

    Returns:
        dict: 有効
        list: 無効（該当ユーザーなし）
    """
    reader = csvfile_to_reader(csvfile)

    # User が存在するかどうかで振り分け
    valid_username_dict = {}
    invalid_username_list = []

    # 1 行ずつデータを取り出し
    for row in reader:
        username = row[0]
        if User.objects.filter(username=username).exists():
            group_list = get_group_list(row)
            valid_username_dict[username] = {
                'user': User.objects.get(username=username),
                'group_list': group_list
            }
        else:
            invalid_username_list.append(username)

    return valid_username_dict, invalid_username_list


def csvfile_to_reader(csvfile):
    """csvfile から reader を作って返す

    header 行は飛ばす
    """
    # reader オブジェクトを作成
    csvtext = io.TextIOWrapper(csvfile)
    reader = csv.reader(csvtext)

    # header 行を pass
    next(reader)

    return reader


def get_group_list(row):
    """CSV 処理で 1 が入っている Group を取得
    """
    return [
        Group.objects.get(groupinfo__order=i)
        for i, data in enumerate(row) if data == '1'
    ]


def file_invalid(request, mode):
    """アップロードしたファイルに不備がある場合の処理
    """
    messages.error(request, 'アップロードしたファイルに不備があります')
    return redirect('home:csv_%s' % mode)


def attach_order(model):
    """Model の object に order を当てる

    order 未割り当てのインスタンスについて order を割り当てる
    """
    # すでに order が割り当てられているインスタンスの order の中で
    # 最も大きい order を取得する。
    # そのような order がない場合は 0 が与えられる。
    max_order = \
        model.objects.all().aggregate(Max('order'))['order__max']

    # まだ order が割り当てられていない (order=0) インスタンスについて
    # order を割り当てていく。
    for counter, unordered_object in enumerate(model.objects.filter(order=0)):
        unordered_object.order = max_order + counter + 1
        unordered_object.save()
