# Generated by Django 3.0.5 on 2020-04-21 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0041_auto_20200421_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='access',
            name='approve_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Request_Access.ApproveList', verbose_name='Лист согласования'),
        ),
        migrations.AlterField(
            model_name='approvelist',
            name='approve_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Request_Access.Service', verbose_name='Сервис'),
        ),
    ]
