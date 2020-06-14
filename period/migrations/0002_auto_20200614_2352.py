# Generated by Django 3.0.7 on 2020-06-14 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('period', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PeriodeThemeSubmit',
            new_name='PeriodThemeFinalVote',
        ),
        migrations.RenameModel(
            old_name='PeriodeThemeFirstVote',
            new_name='PeriodThemeFirstVote',
        ),
        migrations.RenameModel(
            old_name='PeriodeThemeFinalVote',
            new_name='PeriodThemeSubmit',
        ),
        migrations.AlterModelOptions(
            name='periodthemefinalvote',
            options={'verbose_name': '統一テーマ決選投票期間', 'verbose_name_plural': '統一テーマ決選投票期間'},
        ),
        migrations.AlterModelOptions(
            name='periodthemesubmit',
            options={'verbose_name': '統一テーマ応募期間', 'verbose_name_plural': '統一テーマ応募期間'},
        ),
    ]