# Generated by Django 3.2.16 on 2022-12-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]