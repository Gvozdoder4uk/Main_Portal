# Generated by Django 3.0.7 on 2020-08-18 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Request_Access', '0080_bases_1c'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_deps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Департамент или название корневой папки')),
                ('description', models.CharField(blank=True, max_length=140, verbose_name='Описание и назначение')),
                ('owner_filepather', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
            ],
            options={
                'verbose_name': 'Корневая папка файловой шары',
                'verbose_name_plural': 'Корневые папки файловой шары',
            },
        ),
    ]
