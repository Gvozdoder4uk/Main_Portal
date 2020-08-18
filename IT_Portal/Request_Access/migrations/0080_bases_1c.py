# Generated by Django 3.0.7 on 2020-08-18 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0079_auto_20200728_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='bases_1C',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название Базы данных')),
                ('description', models.CharField(blank=True, max_length=140, verbose_name='Описание и назначение базы данных')),
                ('company_attach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Request_Access.Companys', verbose_name='Принадлежность к компании')),
            ],
            options={
                'verbose_name': 'База 1С',
                'verbose_name_plural': 'Базы Данных 1С',
            },
        ),
    ]
