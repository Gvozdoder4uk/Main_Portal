# Generated by Django 3.0.5 on 2020-04-21 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0033_delete_bosses'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_full_name',
            field=models.CharField(max_length=1000, null=True, verbose_name='Полное имя'),
        ),
    ]
