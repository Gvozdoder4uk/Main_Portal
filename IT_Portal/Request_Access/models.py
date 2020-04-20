from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS_CHOICES = (
    ('На согласовании', 'На согласовании'),
    ('Согласовано', 'Согласовано'),
    ('Отказ', 'Заявка отклонена'),
    ('Ошибка', 'Ошибка'),
    ('Пипос', 'Пипос'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_last_name = models.CharField(max_length=200, help_text="Фамилия", verbose_name="Фамилия")
    user_first_name = models.CharField(max_length=200, help_text="Имя", verbose_name="Имя")
    user_second_name = models.CharField(max_length=200, help_text="Отчество", verbose_name="Отчество")
    user_dep = models.CharField(max_length=200, help_text="Департамент", verbose_name="Департамент")
    user_otdel = models.CharField(max_length=200, help_text="Отдел", verbose_name="Отдел")
    user_email = models.EmailField(help_text="Email", verbose_name="Почтовый адрес")
    user_boss = models.CharField(max_length=200, help_text="Руководитель пользователя",
                                 verbose_name="Руководитель пользователя", blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return "%s's profile" % self.user


class Service(models.Model):
    service_name = models.CharField(max_length=200, help_text="Название Сервиса", verbose_name="Название Сервиса")
    service_owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.service_name


# Create your models here.
class Access(models.Model):
    create_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания", null=True)
    name_user = models.CharField(max_length=200, verbose_name="Имя Заявителя")
    user_dep = models.CharField(max_length=200,
                                verbose_name="Департамент пользователя", blank=True, null=True)
    user_otdel = models.CharField(max_length=200, help_text="Отдел пользователя",
                                  verbose_name="Отдел пользователя", blank=True, null=True)
    user_boss = models.CharField(max_length=200,
                                 verbose_name="Руководитель пользователя", blank=True, null=True)
    test_service = models.ForeignKey(Service, on_delete=models.SET_NULL,null=True)
    service_owner = models.CharField(max_length=200, verbose_name="Владелец сервиса")
    ib_spec = models.CharField(max_length=200,
                               verbose_name="Руководитель отдела ИБ")
    request_statuser = models.CharField(max_length=15, choices=STATUS_CHOICES, default='На согласовании')
    request_desc = models.TextField(verbose_name="Описание Запроса")

    class Meta:
        verbose_name = 'Реестр запросов'
        verbose_name_plural = 'Реестр запросов'

    def __str__(self):
        return str(self.id)


class Requests(models.Model):
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    name = models.CharField(max_length=500, verbose_name='Название запроса')
    text = models.TextField(verbose_name='Текст запроса')
    history_of_accept = models.TextField(verbose_name='История соглавания', blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='Дата закрытия заявки', null=True, blank=True)

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return str(self.name)
