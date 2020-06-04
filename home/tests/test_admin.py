from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.test import TestCase

from home.admin import ContactKindAdmin, GroupInfoAdmin
from home.models import ContactKind, GroupInfo


class GroupInfoAdminTestCase(TestCase):
    """[test] GroupTestAdmin

    group_name を検証する
    """
    def setUp(self):
        """Group / GroupInfo を作成
        """
        self.group = Group.objects.create(name='グループ名')
        self.group_info = GroupInfo.objects.create(
            group=self.group,
            email='hoge@hoge.com',
            slack_ch='hoge'
        )

    def test_group_name(self):
        """group_name
        """
        # test group_name
        group_info_admin = GroupInfoAdmin(GroupInfo, ModelAdmin)
        self.assertEqual(
            group_info_admin.group_name(self.group_info), 'グループ名',
            'GroupInfoAdmin に対応する Group.name が正しく表示できません'
        )


class ContactKindAdminTestCase(TestCase):
    """[test] ContactKindAdmin

    list_groups を検証する
    """
    def setUp(self):
        """Group / ContactKind を作成
        """
        # create groups
        group_0 = Group.objects.create(name='グループ名 0')
        group_1 = Group.objects.create(name='グループ名 1')
        group_2 = Group.objects.create(name='グループ名 2')

        # create contact kind
        self.contact_kind = ContactKind.objects.create(name='お問い合わせ種別名')

        # add groups to contact kind
        self.contact_kind.groups.add(*[group_0, group_1, group_2])

    def test_list_groups(self):
        """list_groups
        """
        # test list_groups
        contact_kimd_admin = ContactKindAdmin(ContactKind, ModelAdmin)
        self.assertEqual(
            contact_kimd_admin.list_groups(self.contact_kind),
            'グループ名 0, グループ名 1, グループ名 2',
            'ContactKind.groups が正しく表示できません'
        )
