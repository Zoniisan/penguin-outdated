# Generated by Django 3.0.7 on 2020-06-16 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodThemeFinalVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='開始日時')),
                ('finish', models.DateTimeField(verbose_name='終了日時')),
            ],
            options={
                'verbose_name': '統一テーマ決選投票期間',
                'verbose_name_plural': '統一テーマ決選投票期間',
            },
        ),
        migrations.CreateModel(
            name='PeriodThemeFirstVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='開始日時')),
                ('finish', models.DateTimeField(verbose_name='終了日時')),
            ],
            options={
                'verbose_name': '統一テーマ予選投票期間',
                'verbose_name_plural': '統一テーマ予選投票期間',
            },
        ),
        migrations.CreateModel(
            name='PeriodThemeSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='開始日時')),
                ('finish', models.DateTimeField(verbose_name='終了日時')),
            ],
            options={
                'verbose_name': '統一テーマ応募期間',
                'verbose_name_plural': '統一テーマ応募期間',
            },
        ),
    ]
