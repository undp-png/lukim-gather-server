# Generated by Django 3.2.13 on 2022-06-02 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('has_read', models.BooleanField(db_index=True, default=False, editable=False, verbose_name='read')),
                ('actor_object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='actor object id')),
                ('verb', models.CharField(max_length=100, verbose_name='verb')),
                ('description', models.TextField(verbose_name='description')),
                ('notification_type', models.CharField(default='default', max_length=50, verbose_name='notification type')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('action_object_object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='action object object id')),
                ('target_object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='target object id')),
                ('action_object_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_action_object', to='contenttypes.contenttype', verbose_name='action object content type')),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_actor', to='contenttypes.contenttype', verbose_name='actor content type')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='recipient')),
                ('target_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_target', to='contenttypes.contenttype', verbose_name='target content type')),
            ],
            options={
                'ordering': ('-created_at',),
                'index_together': {('recipient', 'has_read')},
            },
        ),
    ]