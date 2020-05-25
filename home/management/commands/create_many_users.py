"""たくさん User をつくる

検証用のアカウントをたくさん作る。
"""

from django.core.management.base import BaseCommand
from home.models import User


class Command(BaseCommand):
    """[Command] create_many_users

    一般アカウント 200 件と事務局員アカウント 200 件を作成します。
    一般アカウントのうち、shib_faculty = student のものは 100 件、
    faculty のものは 100 件作成されます。

    パスワードはすべて 'hogehoge' です。
    """

    help = '検証用の User をたくさん作ります。'

    def handle(self, *args, **options):
        # 生徒
        for i in range(0, 100):
            zfilled_i = str(i).zfill(2)
            u = User.objects.create(
                username='10000000%s' % zfilled_i,
                last_name='生徒',
                first_name=zfilled_i,
                last_name_kana='せいと',
                first_name_kana='てすと',
                email='test@student%s' % zfilled_i,
                tel='100000000%s' % zfilled_i,
                faculty='総',
                grade='B1',
                shib_eptid='ept_student_%s' % zfilled_i,
                shib_affiliation="student"
            )
            u.set_password('hogehoge')
            u.save()
            self.stdout.write(self.style.SUCCESS('Create(student): "%s"' % u))

        # 先生
        for i in range(0, 100):
            zfilled_i = str(i).zfill(2)
            u = User.objects.create(
                username='20000000%s' % zfilled_i,
                last_name='先生',
                first_name=zfilled_i,
                last_name_kana='せんせい',
                first_name_kana='てすと',
                email='test@faculty%s' % zfilled_i,
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
                email='test@office%s' % zfilled_i,
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
