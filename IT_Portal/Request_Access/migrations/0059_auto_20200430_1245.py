# Generated by Django 3.0.5 on 2020-04-30 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0058_auto_20200430_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvelist',
            name='approve_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Request_Access.Service', verbose_name='Сервис'),
        ),
    ]