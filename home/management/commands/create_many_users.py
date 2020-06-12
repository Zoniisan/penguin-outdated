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
        # 情報
        type_list = [
            {
                'name': '生徒',
                'kana': 'せいと',
                'english': 'student',
                'grade': 'B1',
                'affiliation': 'student'
            },
            {
                'name': '先生',
                'kana': 'せんせい',
                'english': 'faculty',
                'grade': '他',
                'affiliation': 'faculty'
            },
            {
                'name': '事務局員',
                'kana': 'じむきょくいん',
                'grade': 'B1',
                'english': 'officer',
                'affiliation': 'student'
            }
        ]

        # 実際に作成
        for type_id in range(0, 3):
            for i in range(0, 100):
                type_dict = type_list[type_id]
                zfilled_i = str(i).zfill(2)
                u = User.objects.create(
                    username='%s0000000%s' % (str(type_id + 1), zfilled_i),
                    last_name=type_dict['name'],
                    first_name='テスト%s' % zfilled_i,
                    last_name_kana=type_dict['kana'],
                    first_name_kana='てすと',
                    email='%s%s@test.com' %
                    (type_dict['english'], zfilled_i),
                    tel='334%s00000%s' % (str(type_id + 1), zfilled_i),
                    faculty='総',
                    grade=type_dict['grade'],
                    shib_eptid='ept_%s_%s' %
                    (type_dict['english'], zfilled_i),
                    shib_affiliation=type_dict['affiliation']
                )
                u.set_password('hogehoge')
                u.save()
                self.stdout.write(self.style.SUCCESS(
                    'Created(%s): "%s"' % (type_dict['english'], u)
                ))
