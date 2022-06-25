# Generated by Django 3.2.13 on 2022-06-08 06:11

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_alter_legaldocument_document_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, unique=True, verbose_name='identifier')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('html_message', ckeditor.fields.RichTextField(verbose_name='html message')),
                ('text_message', models.TextField(verbose_name='text message')),
            ],
        ),
    ]