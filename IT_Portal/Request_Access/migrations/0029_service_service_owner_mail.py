# Generated by Django 3.0.5 on 2020-04-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0028_auto_20200421_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_owner_mail',
            field=models.EmailField(default='example@yandex.com', max_length=254, verbose_name='Почтовый адрес владельца сервиса'),
            preserve_default=False,
        ),
    ]
