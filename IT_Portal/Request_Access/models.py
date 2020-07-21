from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

# Селектор статусов Согласования
STATUS_CHOICES = (
    ('На согласовании у Руководителя', 'На согласовании у Руководителя'),
    ('Согласовано', 'Согласовано'),
    ('Отказ', 'Заявка отклонена'),
    ('Ошибка', 'Ошибка'),
    ('Пипос', 'Пипос'),
)


# Определение модели пользователя.
# Связка один к одному к модели Пользователь Django
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_last_name = models.CharField(max_length=200, help_text="Фамилия", verbose_name="Фамилия", blank=True)
    user_first_name = models.CharField(max_length=200, help_text="Имя", verbose_name="Имя", blank=True)
    user_second_name = models.CharField(max_length=200, help_text="Отчество", verbose_name="Отчество", blank=True)
    user_full_name = models.CharField(max_length=1000, verbose_name="Полное имя", null=True, blank=True)
    user_position = models.CharField(max_length=300, verbose_name="Должность", null=True, blank=True)
    user_dep = models.CharField(max_length=200, help_text="Департамент", verbose_name="Департамент", blank=True)
    user_otdel = models.CharField(max_length=200, help_text="Отдел", verbose_name="Отдел", blank=True)
    user_email = models.EmailField(help_text="Email", verbose_name="Почтовый адрес", blank=True)
    user_telephone = models.CharField(max_length=30, verbose_name="Внутренний телефон", null=True, blank=True)
    user_mobile = models.CharField(max_length=30, verbose_name="Мобильный телефон", null=True, blank=True)
    user_boss = models.ForeignKey(User, related_name="boss", on_delete=models.CASCADE,
                                  help_text="Руководитель пользователя",
                                  verbose_name="Руководитель пользователя", blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return "%s " % self.user_full_name

    def save(self):
        full_name = str(f"{self.user_last_name} {self.user_first_name} {self.user_second_name}").title()
        self.user_full_name = full_name
        super(UserProfile, self).save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


# Модель сотрудника информационной безопасности. И установка его активным согласующим.
class InformationSecurity(models.Model):
    specialist_ib = models.ForeignKey(User, verbose_name="Специалист Информационной Безопасности",
                                      on_delete=models.CASCADE, null=True, blank=True)
    specialist_ib_email = models.EmailField(verbose_name="Email Специалиста по ИБ")
    spec_ib_podmena = models.ForeignKey(User, verbose_name="Заместитель специалиста по ИБ",
                                        on_delete=models.CASCADE, related_name="Zam")
    active = models.BooleanField(verbose_name="Присвоение")

    class Meta:
        verbose_name = "Специалист Информационной Безопасности"
        verbose_name = "Специалисты Информационной Безопасности"

    def __str__(self):
        return str(self.specialist_ib.userprofile.user_full_name)


# Хранение списка ервисов и ответственных за сервис.
# Service Group для хранения ответственного за группу сервисов

class Service_Group(models.Model):
    group_name = models.CharField(max_length=200)
    group_sowner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сервисная группа'
        verbose_name_plural = 'Сервисные группы'

    def __str__(self):
        return self.group_name


class Service(models.Model):
    service_name = models.CharField(max_length=200, help_text="Название Сервиса", verbose_name="Название Сервиса")
    service_owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    main_owner = models.BooleanField(verbose_name="Главный владелец", default=True)
    service_group = models.ForeignKey(Service_Group, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.service_name


# Модель согласования текущая с учетом 1го сервиса.
class ApproveList(models.Model):
    user_boss = models.CharField(max_length=200, verbose_name="Руководитель пользователя", null=True)
    email_boss = models.EmailField(verbose_name="Почта руководителя")
    approve_status_boss = models.CharField(max_length=200, verbose_name="Статус согласования руководителя",
                                           default="Ожидание согласования")
    ib_spec = models.ForeignKey(InformationSecurity, on_delete=models.CASCADE, verbose_name="Специалист ИБ")
    email_ib = models.EmailField(verbose_name="Почта специалиста IB")
    approve_status_ib = models.CharField(max_length=200, verbose_name="Статус согласования руководителя",
                                         default="Ожидание")
    full_status_request = models.CharField(max_length=200, verbose_name="Статус согласования",
                                           default="Ожидание согласования руководителя")
    change_date = models.DateTimeField(verbose_name="Дата изменения", blank=True, null=True)

    def __str__(self):
        return 'Номер листа:%s Статус заявки: %s' % (self.id, self.full_status_request)


# Main table for Access Request. On This table based ModelForm and Forms.
# Основная таблица хранения заявки.
class Access(models.Model):
    approve_list = models.ForeignKey(ApproveList, on_delete=models.CASCADE, verbose_name="Лист Согласования", null=True,
                                     blank=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания", null=True)
    author = models.ForeignKey(User, max_length=200, verbose_name="Имя Заявителя", on_delete=models.CASCADE, blank=True,
                               null=True)
    user_dep = models.CharField(max_length=200, verbose_name="Департамент пользователя", blank=True, null=True)
    user_otdel = models.CharField(max_length=200, help_text="Отдел пользователя", verbose_name="Отдел пользователя",
                                  blank=True, null=True)
    request_statuser = models.CharField(max_length=100, choices=STATUS_CHOICES,
                                        default='На согласовании у Руководителя')
    request_desc = models.TextField(verbose_name="Описание Запроса")
    creator = models.ForeignKey(User, related_name="Creator", verbose_name="Создатель заявки", on_delete=models.CASCADE,
                                null=True, blank=True)
    comments = models.TextField(max_length=2000, verbose_name="Комментарий к заявке",blank=True, null=True)
    task_flow_history = models.TextField(max_length=5000, verbose_name="История хода заявки", null=True, blank=True)

    class Meta:
        verbose_name = 'Реестр запросов'
        verbose_name_plural = 'Реестр запросов'

    def __str__(self):
        return "%s %s " % (str(self.id), self.author)


# Проектная модель листа согласования
# Утвержденная модель листа согласования сервисной заявки
class List_of_Accept(models.Model):
    # Модель создания множественных листов согласования по каждому сервису.
    Access_ID = models.ForeignKey(Access, verbose_name="Номер Заявки", on_delete=models.CASCADE, null=True, blank=True,
                                  default=40)
    Accepter_FIO = models.CharField(max_length=200, verbose_name="Согласующее лицо", default="Иванов Иван Иванович")
    Accepted_Service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                         verbose_name="Сервис для согласования", default=1)
    Email_Accepter = models.EmailField(verbose_name="Почта согласующего", default="123@mail.rus")
    Accepter_Status = models.CharField(max_length=200, verbose_name="Статус согласования Сервис",
                                       default="Ожидание")

    def __str__(self):
        return "id: %s Номер заявок: %s Согласующее лицо: %s" % (str(self.id), self.Access_ID, self.Accepted_Service)

# Тестовая таблица для запросов, на текущий момент не используется.
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


# Таблица хранения отправленных писем.
class Mails(models.Model):
    email_address = models.EmailField(verbose_name="Получатель")
    subject = models.CharField(max_length=1000, verbose_name="Тема письма")
    message = models.CharField(max_length=20000, verbose_name="Сообщение")

    def __str__(self):
        return self.email


# TEST BLOCK
# FOR EXAMPLES !!!!
# YOU CAN ERASE THAT SHIT
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
