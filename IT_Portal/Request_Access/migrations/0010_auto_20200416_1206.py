# Generated by Django 3.0.5 on 2020-04-16 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0009_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_secondname',
            new_name='user_second_name',
        ),
    ]