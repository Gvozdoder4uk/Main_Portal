# Generated by Django 3.0.5 on 2020-04-16 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0002_auto_20200416_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='access',
            name='ib_spec',
            field=models.CharField(default=1, help_text='Руководитель отдела ИБ', max_length=200, verbose_name='Руководитель отдела ИБ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='access',
            name='user_dir',
            field=models.CharField(default=1, help_text='Руководитель заявителя', max_length=200, verbose_name='Руководитель заявителя'),
            preserve_default=False,
        ),
    ]
