# Generated by Django 3.0.6 on 2020-05-24 23:05

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'その学生番号はすでに使用されています'}, help_text='ハイフン無しの半角数字 10 桁で入力してください', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='半角数字10桁で入力してください', regex='^[0-9]{10}$')], verbose_name='学生番号')),
                ('email', models.EmailField(max_length=400, unique=True, verbose_name='メールアドレス')),
                ('last_name', models.CharField(max_length=50, verbose_name='姓')),
                ('first_name', models.CharField(max_length=50, verbose_name='名')),
                ('last_name_kana', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='ひらがなで入力してください', regex='^[ぁ-んー]+$')], verbose_name='姓（かな）')),
                ('first_name_kana', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='ひらがなで入力してください', regex='^[ぁ-んー]+$')], verbose_name='名（かな）')),
                ('faculty', models.CharField(choices=[('総', '総合人間学部/人間・環境学研究科'), ('文', '文学部/文学研究科'), ('教', '教育学部/教育学研究科'), ('法', '法学部/法学研究科'), ('経', '経済学部/経済学研究科'), ('理', '理学部/理学研究科'), ('医', '医学部/医学研究科'), ('薬', '薬学部/薬学研究科'), ('工', '工学部/工学研究科/情報学研究科'), ('農', '農学部/農学研究科'), ('他', 'その他学部/研究科')], max_length=1, verbose_name='学部/研究科')),
                ('grade', models.CharField(choices=[('B1', '学部1回生'), ('B2', '学部2回生'), ('B3', '学部3回生'), ('B4', '学部4回生'), ('B5+', '学部5回生以上'), ('修士', '修士課程'), ('博士', '博士課程'), ('他', 'その他')], max_length=3, verbose_name='学年')),
                ('tel', models.CharField(help_text='ハイフン無しの半角数字で入力してください', max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='半角数字で入力してください', regex='^[0-9]+$')], verbose_name='電話番号')),
                ('shib_eptid', models.CharField(max_length=400, unique=True, verbose_name='EPTID')),
                ('shib_affiliation', models.CharField(max_length=10, verbose_name='affiliation')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'PENGUIN アカウント',
                'verbose_name_plural': 'PENGUIN アカウント',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
