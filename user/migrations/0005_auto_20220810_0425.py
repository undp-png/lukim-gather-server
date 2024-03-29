# Generated by Django 3.2.14 on 2022-08-10 04:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import lukimgather.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_grant_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=lukimgather.fields.LowerEmailField(blank=True, error_messages={'unique': 'A user with that email already exists.'}, max_length=254, null=True, verbose_name='Email Address'),
        ),
        migrations.CreateModel(
            name='PhoneNumberConfirmationPin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('no_of_incorrect_attempts', models.PositiveIntegerField(default=0, verbose_name='No Of Incorrect Attempts')),
                ('pin', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)], verbose_name='Pin')),
                ('pin_expiry_time', models.DateTimeField(verbose_name='Pin Expiry Time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number_confirm_pin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumberChangePin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('no_of_incorrect_attempts', models.PositiveIntegerField(default=0, verbose_name='No Of Incorrect Attempts')),
                ('pin', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)], verbose_name='Pin')),
                ('pin_expiry_time', models.DateTimeField(verbose_name='Pin Expiry Time')),
                ('new_email', lukimgather.fields.LowerEmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number_change_pin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
