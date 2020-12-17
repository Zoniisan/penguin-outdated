# Generated by Django 3.0.7 on 2020-06-18 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100, verbose_name='団体名')),
                ('group_name_kana', models.CharField(max_length=100, verbose_name='団体名（かな）')),
                ('food', models.BooleanField(default=False, verbose_name='飲食物提供')),
                ('short_description', models.CharField(help_text='簡潔に内容を説明してください。暫定的な内容で構いません。', max_length=100, verbose_name='企画概要')),
                ('call_id', models.SlugField(max_length=4, verbose_name='呼び出しコード')),
                ('status', models.CharField(choices=[('waiting', '待機中'), ('calling', '呼出中'), ('handling', '対応中'), ('accepted', '登録完了'), ('invalid', '無効')], max_length=10, verbose_name='状態')),
                ('token', models.CharField(max_length=50, null=True, verbose_name='トークン')),
                ('register_datetime', models.DateTimeField(null=True, verbose_name='登録完了日時')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='企画種別')),
                ('registerant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_registerant', to=settings.AUTH_USER_MODEL, verbose_name='登録者')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_staff', to=settings.AUTH_USER_MODEL, verbose_name='登録スタッフ')),
            ],
            options={
                'verbose_name': '企画登録',
                'verbose_name_plural': '企画登録',
            },
        ),
    ]
