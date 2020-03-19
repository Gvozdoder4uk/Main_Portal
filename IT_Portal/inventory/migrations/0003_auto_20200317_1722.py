# Generated by Django 3.0.4 on 2020-03-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventory_bd_network_mac'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory_bd',
            name='name_pc',
            field=models.CharField(default=0, help_text='Доменное имя ПК', max_length=200, verbose_name='Имя ПК'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='network_card',
            field=models.CharField(default=1, help_text='Сетевуха', max_length=200, verbose_name='Сетевая карточка'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='os',
            field=models.CharField(default=1, help_text='ОСЬ', max_length=200, verbose_name='Опреционная система'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='owner',
            field=models.CharField(default=1, help_text='Владелец ПК', max_length=200, verbose_name='Владелец ПК'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='processor',
            field=models.CharField(default=1, help_text='Проц', max_length=200, verbose_name='Процессор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='ram_type',
            field=models.CharField(default=1, help_text='Тип ОЗУ', max_length=200, verbose_name='Тип ОЗУ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory_bd',
            name='sum_ram',
            field=models.IntegerField(default=1, help_text='Сумма оперативки', max_length=10, verbose_name='ОЗУ'),
            preserve_default=False,
        ),
    ]
