# Generated by Django 3.2.13 on 2022-05-10 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_auto_20220504_0614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys'},
        ),
        migrations.RemoveField(
            model_name='survey',
            name='order',
        ),
        migrations.AddField(
            model_name='survey',
            name='answer',
            field=models.JSONField(blank=True, default=dict, verbose_name='answer'),
        ),
        migrations.DeleteModel(
            name='SurveyAnswer',
        ),
    ]
