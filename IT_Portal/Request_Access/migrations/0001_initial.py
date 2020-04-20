# Generated by Django 3.0.5 on 2020-04-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_access', models.CharField(help_text='Номер Заявки', max_length=30, verbose_name='Номер заявки')),
                ('name_user', models.CharField(help_text='Имя Заявителя', max_length=200, verbose_name='Имя Заявителя')),
                ('service', models.CharField(help_text='Сервис', max_length=100, verbose_name='Сервис')),
                ('service_owner', models.CharField(help_text='Владелец сервиса', max_length=200, verbose_name='Владелец сервиса')),
                ('request', models.TextField(help_text='Описание Запроса', verbose_name='Описание Запроса')),
            ],
            options={
                'verbose_name': 'Реестр запросов',
                'verbose_name_plural': 'Реестр запросов',
            },
        ),
    ]
