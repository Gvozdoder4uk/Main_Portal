# Generated by Django 3.0.5 on 2020-04-19 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0013_auto_20200419_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requests',
            options={'verbose_name': 'Запрос', 'verbose_name_plural': 'Запросы'},
        ),
        migrations.AddField(
            model_name='requests',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия заявки'),
        ),
        migrations.AddField(
            model_name='requests',
            name='history_of_accept',
            field=models.TextField(blank=True, null=True, verbose_name='История соглавания'),
        ),
    ]
