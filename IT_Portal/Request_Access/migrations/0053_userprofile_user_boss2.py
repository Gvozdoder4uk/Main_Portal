# Generated by Django 3.0.5 on 2020-04-28 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Request_Access', '0052_auto_20200427_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_boss2',
            field=models.ForeignKey(blank=True, help_text='Руководитель пользователя', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boss', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель пользователя'),
        ),
    ]
