"""たくさん User をつくる

検証用のアカウントをたくさん作る。
"""

from django.core.management.base import BaseCommand
from home.models import User


class Command(BaseCommand):
    """[Command] create_many_users

    User モデルを大量に作成します。学生番号は
    10000000[0-9]{2}: 一般京大生
    20000000[0-9]{2}: 教授など（shib_affiliation='faculty')
    30000000[0-9]{2}: 事務局員
    です。ただし、事務局員のスタッフ権限は CSV 機能を用いて与えるため、
    ここでは一般アカウントとして作成します。
    また、システム管理者（スーパーユーザー）は manage.py createsuperuser
    で作成することが想定されているため、ここでは作成しません。

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
                first_name='テスト%s' % zfilled_i,
                last_name_kana='せいと',
                first_name_kana='てすと',
                email='student%s@test.com' % zfilled_i,
                tel='334100000%s' % zfilled_i,
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
                first_name='テスト%s' % zfilled_i,
                last_name_kana='せんせい',
                first_name_kana='てすと',
                email='faculty%s@test.com' % zfilled_i,
                tel='334200000%s' % zfilled_i,
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
                first_name='テスト%s' % zfilled_i,
                last_name_kana='じむきょくいん',
                first_name_kana='てすと',
                email='office%s@test.com' % zfilled_i,
                tel='334300000%s' % zfilled_i,
                faculty='総',
                grade='B1',
                shib_eptid='ept_officer_%s' % zfilled_i,
                shib_affiliation="student",
            )
            u.set_password('hogehoge')
            u.save()
            self.stdout.write(self.style.SUCCESS('Create(office): "%s"' % u))
