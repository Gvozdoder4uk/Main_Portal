# Generated by Django 3.0.7 on 2020-07-22 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0076_auto_20200722_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='companys',
            name='company_activator',
            field=models.BooleanField(blank=True, help_text='Установка триггера владельца портала', null=True, verbose_name='Владелец портала'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Request_Access.Companys', verbose_name='Компания пользователя'),
            preserve_default=False,
        ),
    ]
