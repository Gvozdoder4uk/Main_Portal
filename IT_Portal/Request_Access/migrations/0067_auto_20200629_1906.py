# Generated by Django 3.0.5 on 2020-06-29 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0066_auto_20200629_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_of_accept',
            name='Accepted_Service',
            field=models.CharField(max_length=200, null=True, verbose_name='Сервис для согласования'),
        ),
    ]