# Generated by Django 3.0.5 on 2020-04-22 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0046_address_store'),
    ]

    operations = [
        migrations.RenameField(
            model_name='access',
            old_name='number_task',
            new_name='approve_list',
        ),
        migrations.RemoveField(
            model_name='approvelist',
            name='number_task',
        ),
    ]