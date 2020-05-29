"""検証環境向けにテスト用のデータを作成する

"""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from home.models import ContactKind, GroupInfo, User


class Command(BaseCommand):
    """[Command] create_models_for_dev

    検証用のモデルを作成します。
    User のパスワードはすべて 'hogehoge' です。
    """

    help = '検証用のモデルを作ります。'

    def handle(self, *args, **options):
        # User - スーパーユーザー
        u = User.objects.create(
            username='9000000000',
            last_name='時乃',
            first_name='空',
            last_name_kana='ときの',
            first_name_kana='そら',
            email='tokino@sora.com',
            tel='9000000000',
            faculty='総',
            grade='B1',
            shib_eptid='ept_tokinosora',
            shib_affiliation="student",
            is_staff=True,
            is_superuser=True
        )
        u.set_password('hogehoge')
        u.save()
        self.stdout.write(self.style.SUCCESS('Create(superuser): "%s"' % u))

        # User - 生徒
        for i in range(0, 100):
            zfilled_i = str(i).zfill(2)
            u = User.objects.create(
                username='10000000%s' % zfilled_i,
                last_name='生徒',
                first_name=zfilled_i,
                last_name_kana='せいと',
                first_name_kana='てすと',
                email='test@student%s.com' % zfilled_i,
                tel='100000000%s' % zfilled_i,
                faculty='総',
                grade='B1',
                shib_eptid='ept_student_%s' % zfilled_i,
                shib_affiliation="student"
            )
            u.set_password('hogehoge')
            u.save()
            self.stdout.write(self.style.SUCCESS('Create(student): "%s"' % u))

        # User - 先生
        for i in range(0, 100):
            zfilled_i = str(i).zfill(2)
            u = User.objects.create(
                username='20000000%s' % zfilled_i,
                last_name='先生',
                first_name=zfilled_i,
                last_name_kana='せんせい',
                first_name_kana='てすと',
                email='test@faculty%s.com' % zfilled_i,
                tel='20000000%s' % zfilled_i,
                faculty='総',
                grade='他',
                shib_eptid='ept_faculty_%s' % zfilled_i,
                shib_affiliation="faculty"
            )
            u.set_password('hogehoge')
            u.save()
            self.stdout.write(self.style.SUCCESS('Create(faculty): "%s"' % u))

        # 事務局員
        for i in range(0, 100):
            zfilled_i = str(i).zfill(2)
            u = User.objects.create(
                username='30000000%s' % zfilled_i,
                last_name='事務局員',
                first_name=zfilled_i,
                last_name_kana='じむきょくいん',
                first_name_kana='てすと',
                email='test@office%s.com' % zfilled_i,
                tel='30000000%s' % zfilled_i,
                faculty='総',
                grade='B1',
                shib_eptid='ept_officer_%s' % zfilled_i,
                shib_affiliation="student",
                is_staff=True
            )
            u.set_password('hogehoge')
            u.save()
            self.stdout.write(self.style.SUCCESS('Create(office): "%s"' % u))

        # Group
        g1 = Group.objects.create(name='システム担当')
        g1.save()
        self.stdout.write(self.style.SUCCESS('Create(Group): "%s"' % g1))
        g2 = Group.objects.create(name='幹部')
        g2.save()
        self.stdout.write(self.style.SUCCESS('Create(Group): "%s"' % g2))

        # GroupInfo
        gi1 = GroupInfo.objects.create(
            name='システム担当',
            group=g1,
            email='system@example.com',
            slack_ch='system'
        )
        gi1.save()
        self.stdout.write(
            self.style.SUCCESS('Create(GroupInfo): "%s"' % gi1)
        )
        gi2 = GroupInfo.objects.create(
            name='幹部',
            group=g2,
            email='knb@example.com',
            slack_ch='knb'
        )
        gi2.save()
        self.stdout.write(
            self.style.SUCCESS('Create(GroupInfo): "%s"' % gi2)
        )

        # ContactKind
        c1 = ContactKind.objects.create(
            name='11 月祭全般について'
        )
        c1.groups.add(g1)
        c1.groups.add(g2)
        c1.save()
        self.stdout.write(self.style.SUCCESS('Create(ContactKind): "%s"' % c1))
        c2 = ContactKind.objects.create(
            name='バグ報告'
        )
        c2.groups.add(g1)
        c2.save()
        self.stdout.write(self.style.SUCCESS('Create(ContactKind): "%s"' % c2))
        c3 = ContactKind.objects.create(
            name='個人情報の変更依頼'
        )
        c3.groups.add(g1)
        c3.save()
        self.stdout.write(self.style.SUCCESS('Create(ContactKind): "%s"' % c3))

        # 部局担当割り当て
        u1 = User.objects.get(username='9000000000')
        u1.groups.add(g1)
        u1.save()
        u2 = User.objects.get(username='3000000000')
        u2.groups.add(g1)
        u2.save()
        u3 = User.objects.get(username='3000000001')
        u3.groups.add(g1)
        u3.save()
        u4 = User.objects.get(username='3000000010')
        u4.groups.add(g2)
        u4.save()
        u5 = User.objects.get(username='3000000011')
        u5.groups.add(g2)
        u5.save()
