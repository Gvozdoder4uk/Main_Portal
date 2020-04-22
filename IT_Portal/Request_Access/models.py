from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

STATUS_CHOICES = (
    ('На согласовании у Руководителя', 'На согласовании у Руководителя'),
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
    user_full_name = models.CharField(max_length=1000, verbose_name="Полное имя", null=True)
    user_dep = models.CharField(max_length=200, help_text="Департамент", verbose_name="Департамент")
    user_otdel = models.CharField(max_length=200, help_text="Отдел", verbose_name="Отдел")
    user_email = models.EmailField(help_text="Email", verbose_name="Почтовый адрес")
    user_boss = models.CharField(max_length=200, help_text="Руководитель пользователя",
                                 verbose_name="Руководитель пользователя", blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return "%s " % self.user_full_name


class InformationSecurity(models.Model):
    specialist_ib = models.ForeignKey(UserProfile, verbose_name="Специалист Информационной Безопасности",
                                      on_delete=models.CASCADE)
    specialist_ib_email = models.EmailField(verbose_name="Email Специалиста по ИБ")
    spec_ib_podmena = models.ForeignKey(UserProfile, verbose_name="Заместитель специалиста по ИБ",
                                        on_delete=models.CASCADE, related_name="Zam")
    active = models.BooleanField(verbose_name="Присвоение")

    class Meta:
        verbose_name = "Специалист Информационной Безопасности"
        verbose_name = "Специалисты Информационной Безопасности"

    def __str__(self):
        return str(self.specialist_ib)


class Service(models.Model):
    service_name = models.CharField(max_length=200, help_text="Название Сервиса", verbose_name="Название Сервиса")
    service_owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    main_owner = models.BooleanField(verbose_name="Главный владелец", default=True)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.service_name


class ApproveList(models.Model):
    approve_service = models.ForeignKey(Service, verbose_name="Сервис", on_delete=models.CASCADE)
    service_owner = models.CharField(max_length=200, verbose_name="Владелец Сервиса")
    email_service_owner = models.EmailField(verbose_name="Почта владельца сервиса")
    approve_status_owner = models.CharField(max_length=200, verbose_name="Статус согласования Сервис",
                                            default="Ожидание")
    user_boss = models.CharField(max_length=200, verbose_name="Руководитель пользователя", null=True)
    email_boss = models.EmailField(verbose_name="Почта руководителя")
    approve_status_boss = models.CharField(max_length=200, verbose_name="Статус согласования руководителя",
                                           default="Ожидание согласования")
    ib_spec = models.ForeignKey(InformationSecurity, on_delete=models.CASCADE, verbose_name="Специалист ИБ")
    email_ib = models.EmailField(verbose_name="Почта специалиста IB")
    approve_status_ib = models.CharField(max_length=200, verbose_name="Статус согласования руководителя",
                                         default="Ожидание")
    fileserver_owner = models.CharField(max_length=200, verbose_name="Владелец Файловой помойки", blank=True, null=True)
    email_fileserver = models.EmailField(verbose_name="Почта Владельца Файлового хранилища", blank=True, null=True)
    full_status_request = models.CharField(max_length=200, verbose_name="Статус согласования",
                                           default="Ожидание согласования руководителя")
    change_date = models.DateTimeField(verbose_name="Дата изменения", blank=True, null=True)

    def __str__(self):
        return str(self.id)


# Create your models here.
class Access(models.Model):
    approve_list = models.ForeignKey(ApproveList, on_delete=models.CASCADE, verbose_name="Номер заявки",null=True,blank=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания", null=True)
    name_user = models.CharField(max_length=200, verbose_name="Имя Заявителя")
    user_dep = models.CharField(max_length=200,
                                verbose_name="Департамент пользователя", blank=True, null=True)
    user_otdel = models.CharField(max_length=200, help_text="Отдел пользователя",
                                  verbose_name="Отдел пользователя", blank=True, null=True)
    request_statuser = models.CharField(max_length=100, choices=STATUS_CHOICES,
                                        default='На согласовании у Руководителя')
    request_desc = models.TextField(verbose_name="Описание Запроса")

    class Meta:
        verbose_name = 'Реестр запросов'
        verbose_name_plural = 'Реестр запросов'

    def __str__(self):
        return "%s %s " % (str(self.id), self.name_user)


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


class Mails(models.Model):
    email_address = models.EmailField(verbose_name="Получатель")
    subject = models.CharField(max_length=1000, verbose_name="Тема письма")
    message = models.CharField(max_length=20000, verbose_name="Сообщение")

    def __str__(self):
        return self.email


class Address(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=140, blank=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)