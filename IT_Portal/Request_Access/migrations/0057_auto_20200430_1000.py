# Generated by Django 3.0.5 on 2020-04-30 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Request_Access', '0056_userprofile_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='creator',
        ),
        migrations.AddField(
            model_name='access',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель заявки'),
        ),
    ]
