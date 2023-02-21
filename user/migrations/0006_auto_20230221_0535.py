# Generated by Django 3.2.18 on 2023-02-21 05:35

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220810_0425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumberchangepin',
            name='new_email',
        ),
        migrations.AddField(
            model_name='phonenumberchangepin',
            name='new_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, region=None),
        ),
    ]
