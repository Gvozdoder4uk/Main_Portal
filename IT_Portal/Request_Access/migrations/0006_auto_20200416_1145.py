# Generated by Django 3.0.5 on 2020-04-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль Пользователя', 'verbose_name_plural': 'Реестр запросов'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_dep',
            field=models.CharField(default=1, help_text='Департамент', max_length=200, verbose_name='Департамент'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_email',
            field=models.EmailField(default=1, help_text='Email', max_length=254, verbose_name='Почтовый адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_first_name',
            field=models.CharField(default=1, help_text='Имя', max_length=200, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_last_name',
            field=models.CharField(default=1, help_text='Фамилия', max_length=200, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_otdel',
            field=models.CharField(default=1, help_text='Отдел', max_length=200, verbose_name='Отдел'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_secondname',
            field=models.CharField(default=1, help_text='Отчество', max_length=200, verbose_name='Отчество'),
            preserve_default=False,
        ),
    ]
