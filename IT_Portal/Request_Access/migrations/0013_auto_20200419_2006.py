# Generated by Django 3.0.5 on 2020-04-19 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Request_Access', '0012_auto_20200418_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('name', models.CharField(max_length=500, verbose_name='Название запроса')),
                ('text', models.TextField(verbose_name='Текст запроса')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(help_text='Название Сервиса', max_length=200, verbose_name='Название Сервиса')),
                ('service_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Request_Access.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='access',
            name='test_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Request_Access.Service'),
        ),
    ]
