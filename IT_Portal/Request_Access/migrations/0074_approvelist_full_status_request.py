# Generated by Django 3.0.5 on 2020-07-02 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0073_auto_20200702_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvelist',
            name='full_status_request',
            field=models.CharField(default='Ожидание согласования руководителя', max_length=200, verbose_name='Статус согласования'),
        ),
    ]
