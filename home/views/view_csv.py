import csv
import io

from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic

from home import forms
from home.models import ContactKind, GroupInfo, User
from penguin import mixins


class CsvGroupView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    フォーム画面
    """

    template_name = 'home/csv_group.html'
    form_class = forms.CsvForm


class CsvGroupConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 登録できる情報とできない情報に振り分ける
        valid_group_dict, invalid_group_dict = csv_group_to_dict(csvfile)

        return render(
            self.request, 'home/csv_group_confirm.html', {
                'form': form,
                'valid_group_dict': valid_group_dict,
                'invalid_group_dict': invalid_group_dict
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_group')


class CsvGroupSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Group, GroupInfo を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

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

        return render(
            self.request, 'home/csv_group_success.html', {
                'group_list': Group.objects.all(),
                'created_group_pk_list': created_group_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_group')


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


def csv_group_download(request):
    """[CSV] Group, GroupInfo を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="group.csv"'

    # CSV 書き出し
    writer = csv.writer(response)
    writer.writerow([
        'Group.name（例：総合対応局 システム担当）',
        'GroupInfo.email（例：system@example.com）',
        'GroupInfo.slack_ch（例：st-system）'
    ])

    return response


class CsvContactKindView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    フォーム画面
    """

    template_name = 'home/csv_contact_kind.html'
    form_class = forms.CsvForm


class CsvContactKindConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        contact_kind_dict = csv_contact_kind_to_dict(csvfile)

        return render(
            self.request, 'home/csv_contact_kind_confirm.html', {
                'form': form,
                'contact_kind_dict': contact_kind_dict
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


class CsvContactKindSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] ContactKind を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

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

        return render(
            self.request, 'home/csv_contact_kind_success.html', {
                'contact_kind_list': ContactKind.objects.all(),
                'created_contact_kind_pk_list': created_contact_kind_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


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


def csv_contact_kind_download(request):
    """[CSV] ContactKind を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="contact_kind.csv"'

    # CSV 書き出し
    writer = csv.writer(response)

    # 部局担当リスト（管轄する部局の欄に 1 を入力する）
    group_list = list(
        Group.objects.all().order_by(
            'groupinfo'
        ).values_list(
            'name', flat=True
        )
    )

    # データ書き出し
    writer.writerow(
        ['ContactKind.name（例：11 月祭全般についてのお問い合わせ）'] + group_list
    )

    return response


class CsvStaffRegisterView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Staff User を作成

    フォーム画面
    """

    template_name = 'home/csv_staff_register.html'
    form_class = forms.CsvForm


class CsvStaffRegisterConfirmView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] Staff User を作成

    確認画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

        # 情報を取得
        valid_user_dict, invalid_user_list \
            = csv_staff_register_to_dict(csvfile)

        return render(
            self.request, 'home/csv_staff_register_confirm.html', {
                'form': form,
                'valid_user_dict': valid_user_dict,
                'invalid_user_list': invalid_user_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


class CsvStaffRegisterSuccessView(mixins.AdminOnlyMixin, generic.FormView):
    """[CSV] StaffRegister を作成

    完了画面
    """

    form_class = forms.CsvForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['csvfile']

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

        return render(
            self.request, 'home/csv_staff_register_success.html', {
                'object_list': [
                    {
                        'group': group,
                        'member_list': group.user_set.all().order_by(
                            '-grade', 'last_name_kana', 'first_name_kana'
                        )
                    }
                    for group in Group.objects.all().order_by(
                        'groupinfo__order'
                    )
                ],
                'created_staff_register_pk_list':
                    created_staff_register_pk_list
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, 'アップロードしたファイルに不備があります')
        return redirect('home:csv_contact_kind')


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


def csv_staff_register_download(request):
    """[CSV] StaffRegister を作成

    テンプレート CSV ファイルダウンロード
    """

    # アクセスはシステム管理者のみ
    if not request.user.is_superuser:
        raise PermissionDenied

    # ファイルはサーバーに残さない（危なっかしいので）
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = \
        'attachment; filename="staff_register.csv"'

    # CSV 書き出し
    writer = csv.writer(response)

    # 部局担当リスト（管轄する部局の欄に 1 を入力する）
    group_list = list(
        Group.objects.all().order_by(
            'groupinfo'
        ).values_list(
            'name', flat=True
        )
    )

    # データ書き出し
    writer.writerow(
        ['User.username（例：1029290000）'] + group_list
    )

    return response
