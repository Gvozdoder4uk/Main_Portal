# Generated by Django 3.0.7 on 2020-07-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0074_approvelist_full_status_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='access',
            name='comments',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='Комментарий к заявке'),
        ),
        migrations.AddField(
            model_name='access',
            name='task_flow_history',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='История хода заявки'),
        ),
    ]