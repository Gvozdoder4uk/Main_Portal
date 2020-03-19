from django.db import models


# Create your models here.

class inventory_BD(models.Model):
    name_pc = models.CharField(max_length=200, help_text="Доменное имя ПК", verbose_name="Имя ПК")
    owner = models.CharField(max_length=200, help_text="Владелец ПК", verbose_name="Владелец ПК")
    os = models.CharField(max_length=200, help_text="ОСЬ", verbose_name="Опреционная система")
    processor = models.CharField(max_length=200, help_text="Проц", verbose_name="Процессор")
    sum_ram = models.IntegerField(max_length=10, help_text="Сумма оперативки", verbose_name="ОЗУ")
    ram_type = models.CharField(max_length=200, help_text="Тип ОЗУ", verbose_name="Тип ОЗУ")
    network_card = models.CharField(max_length=200, help_text="Сетевуха", verbose_name="Сетевая карточка")
    network_Mac = models.CharField(max_length=200, help_text="Мак Сетевухи", verbose_name="Мак Адрес")

    def __str__(self):
        return self.name_pc


class services(models.Model):
    service_name = models.CharField(max_length=200, help_text="Название сервиса", verbose_name="Сервис"),


class Ad_users(models.Model):
    user_lastname = models.CharField('Фамилия', max_length=200, help_text="Фамилия пользователя")
    user_firstname = models.CharField('Имя', max_length=200, help_text="Имя пользователя")
    user_secondname = models.CharField('Отчество', max_length=200, help_text="Фамилия пользователя")
    user_birth = models.DateField('Дата рождения', help_text="Дата рождения")
    user_photo = models.ImageField('Фото', help_text="Фото пользователя")
    user_dep = models.CharField('Департамент', max_length=500, help_text="Департамент")
    user_otdel = models.CharField('Отдел', max_length=500, help_text="Отдел пользователя")
    user_desc = models.TextField('Коментарии', max_length=1000,help_text="Дополнительная информация")

    def __str__(self):
        return '%s %s ' % (self.user_firstname, self.user_lastname)
