# Generated by Django 3.2.13 on 2022-05-03 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20220428_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='form',
            options={'ordering': ('order',), 'verbose_name': 'Form', 'verbose_name_plural': 'Forms'},
        ),
        migrations.AlterModelOptions(
            name='happeningsurvey',
            options={'ordering': ['-created_at'], 'verbose_name': 'Happening survey', 'verbose_name_plural': 'Happening surveys'},
        ),
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ('order',), 'verbose_name': 'Option', 'verbose_name_plural': 'Options'},
        ),
        migrations.AlterModelOptions(
            name='protectedareacategory',
            options={'verbose_name': 'Protected area category', 'verbose_name_plural': 'Protected area categories'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('order',), 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questiongroup',
            options={'ordering': ('order',), 'verbose_name': 'Question group', 'verbose_name_plural': 'Question groups'},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ('order',), 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys'},
        ),
    ]