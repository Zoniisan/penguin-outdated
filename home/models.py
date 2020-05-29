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


class GroupInfo(models.Model):
    """ 事務局員の部局担当情報
    """

    # settings

    class Meta:
        verbose_name = '部局担当情報'
        verbose_name_plural = verbose_name
        ordering = ('order',)

    def __str__(self):
        return self.group.name

    # fields

    group = models.OneToOneField(
        'auth.Group',
        verbose_name='authGroup',
        on_delete=models.CASCADE
    )

    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=200
    )

    slack_ch = models.CharField(
        verbose_name='slack channel',
        max_length=100,
        unique=True
    )

    order = models.PositiveIntegerField(
        default=0
    )


class Notice(models.Model):
    """ ホーム画面に表示される「お知らせ」
    """

    # settings

    class Meta:
        verbose_name = 'お知らせ'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # fields

    title = models.CharField(
        verbose_name='タイトル',
        max_length=30,
        help_text='30 文字以内で入力してください。'
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=100,
        help_text='100 文字以内で入力してください。あまり長い文章は好ましくありません。'
    )

    writer = models.ForeignKey(
        'home.User',
        verbose_name='入力者',
        on_delete=models.SET_NULL,
        null=True
    )

    update_datetime = models.DateTimeField(
        verbose_name='最終更新日時',
        auto_now=True
    )


class Contact(models.Model):
    """お問い合わせ
    """

    # settings

    class Meta:
        verbose_name = 'お問い合わせ'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # fields
    title = models.CharField(
        verbose_name='表題',
        max_length=100
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=2000
    )

    kind = models.ForeignKey(
        'home.ContactKind',
        verbose_name='お問い合わせ種別',
        on_delete=models.CASCADE
    )

    writer = models.ForeignKey(
        'home.User',
        verbose_name='入力者',
        on_delete=models.CASCADE
    )

    create_datetime = models.DateTimeField(
        verbose_name='作成日時',
        auto_now_add=True
    )


class ContactKind(models.Model):
    """お問い合わせ種別
    """

    # settings

    class Meta:
        verbose_name = 'お問い合わせ種別'
        verbose_name_plural = verbose_name
        ordering = ('order',)

    def __str__(self):
        return self.name

    # fields

    name = models.CharField(
        verbose_name='種別名',
        max_length=100
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='管轄'
    )

    order = models.PositiveIntegerField(
        default=0
    )


class Notification(models.Model):
    """通知
    """

    # settings

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def has_read(self, user):
        """ある User がすでに通知を呼んだかどうかを判定する

        NotificationRead がヒットするかどうかを返す
        """
        return self.notificationread_set.filter(
            user=user
        ).exists()

    # fields

    title = models.CharField(
        verbose_name='表題',
        max_length=50
    )

    body = models.TextField(
        verbose_name='本文',
        max_length=2000
    )

    to = models.ManyToManyField(
        'home.User',
        verbose_name='宛先',
        related_name='notification_to'
    )

    sender = models.ForeignKey(
        'home.User',
        verbose_name='送信者',
        on_delete=models.CASCADE,
        related_name='notification_from'
    )

    group = models.ForeignKey(
        'auth.Group',
        verbose_name='担当',
        on_delete=models.CASCADE,
        help_text='どの担当として送信するかをここで選択してください。',
    )

    create_datetime = models.DateTimeField(
        verbose_name='送信日時',
        auto_now_add=True
    )


class NotificationRead(models.Model):
    """通知既読情報
    """

    # settings

    class Meta:
        verbose_name = '通知既読'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.notification)

    # fields
    notification = models.ForeignKey(
        'home.Notification',
        verbose_name='通知',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'home.User',
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    create_datetime = models.DateTimeField(
        verbose_name='開封日時',
        auto_now_add=True
    )
