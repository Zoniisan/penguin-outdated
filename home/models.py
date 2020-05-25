from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """ PENGUIN アカウント
    """

    # settings

    class Meta:
        verbose_name = 'PENGUIN アカウント'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_full_name() + ' (' + self.username + ')'

    # functions

    def get_full_name(self):
        """フルネームを返す
        """
        return "".join([self.last_name, self.first_name])

    def get_display_name(self):
        """表示名を返す
        """
        return '(' + self.faculty + '/' + self.grade + ') ' \
            + self.get_full_name()

    # validators

    username_validator = RegexValidator(
        regex=(r'^[0-9]{10}$'),
        message=('半角数字10桁で入力してください')
    )

    kana_validator = RegexValidator(
        regex=(r'^[ぁ-んー]+$'),
        message=('ひらがなで入力してください')
    )

    digit_validator = RegexValidator(
        regex=(r'^[0-9]+$'),
        message=('半角数字で入力してください')
    )

    # choices

    faculty_choices = (
        ('総', '総合人間学部/人間・環境学研究科'),
        ('文', '文学部/文学研究科'),
        ('教', '教育学部/教育学研究科'),
        ('法', '法学部/法学研究科'),
        ('経', '経済学部/経済学研究科'),
        ('理', '理学部/理学研究科'),
        ('医', '医学部/医学研究科'),
        ('薬', '薬学部/薬学研究科'),
        ('工', '工学部/工学研究科/情報学研究科'),
        ('農', '農学部/農学研究科'),
        ('他', 'その他学部/研究科'),
    )

    grade_choices = (
        ('B1', '学部1回生'),
        ('B2', '学部2回生'),
        ('B3', '学部3回生'),
        ('B4', '学部4回生'),
        ('B5+', '学部5回生以上'),
        ('修士', '修士課程'),
        ('博士', '博士課程'),
        ('他', 'その他'),
    )

    # fields

    username = models.CharField(
        verbose_name='学生番号',
        max_length=10,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('その学生番号はすでに使用されています')
        },
        help_text='ハイフン無しの半角数字 10 桁で入力してください'
    )

    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=400,
        unique=True
    )

    last_name = models.CharField(
        verbose_name='姓',
        max_length=50
    )

    first_name = models.CharField(
        verbose_name='名',
        max_length=50
    )

    last_name_kana = models.CharField(
        verbose_name='姓（かな）',
        max_length=50,
        validators=[kana_validator]
    )

    first_name_kana = models.CharField(
        verbose_name='名（かな）',
        max_length=50,
        validators=[kana_validator]
    )

    faculty = models.CharField(
        verbose_name='学部/研究科',
        max_length=1,
        choices=faculty_choices
    )

    grade = models.CharField(
        verbose_name='学年',
        max_length=3,
        choices=grade_choices
    )

    tel = models.CharField(
        max_length=11,
        validators=[digit_validator],
        verbose_name='電話番号',
        help_text='ハイフン無しの半角数字で入力してください',
        unique=True
    )

    shib_eptid = models.CharField(
        verbose_name='EPTID',
        max_length=400,
        unique=True
    )

    shib_affiliation = models.CharField(
        verbose_name='affiliation',
        max_length=10
    )


class UserToken(models.Model):
    """ PENGUIN アカウント仮登録トークン

    トークンは 1 時間有効
    """

    # settings

    class Meta:
        verbose_name = '仮登録トークン'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email

    # fields

    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=400
    )

    token = models.CharField(
        verbose_name='トークン',
        max_length=100
    )

    create_datetime = models.DateTimeField(
        verbose_name='仮登録日時',
        auto_now_add=True
    )

    used = models.BooleanField(
        verbose_name='使用済',
        default=False
    )
