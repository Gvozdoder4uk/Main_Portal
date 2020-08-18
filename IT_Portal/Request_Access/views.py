from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from datetime import *
import platform
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import time
from django.core.files.storage import FileSystemStorage
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage


def is_member(user):
    return user.groups.filter(name='Admin Reestr').exists()


@login_required
def cabinet(request):
    if request.user.groups.filter(name='Admin Reestr').exists():
        service_requests = List_of_Accept.objects.all()
        all_requests_pag = Access.objects.all().order_by('-create_date')
        paginator = Paginator(all_requests_pag, 25)
        page = request.GET.get('page')
        try:
            all_requests = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_requests = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_requests = paginator.page(paginator.num_pages)
        context = {
            'all_requests': all_requests,
            'service_requests': service_requests
        }
        return render(request, 'request_access/cabinet.html', context)
    else:
        return render(request, 'Main_templates/404.html')


@login_required
def personal_cabinet(request):
    user_requests = Access.objects.filter(author=request.user)
    service_requests = List_of_Accept.objects.all()
    context = {
        'user_requests': user_requests,
        'service_requests': service_requests
    }
    return render(request, 'request_access/personal_request.html', context)


@login_required
def account(request):
    return render(request, 'request_access/account.html')


class RequestListView(ListView):
    model = Requests
    template_name = 'request_access/test_request.html'
    context_object_name = 'all_tasks'


class RequestDetailView(DetailView):
    model = Requests
    template_name = 'request_access/detail_request.html'
    context_object_name = 'get_request'


@login_required
def accepted_requests(request):
    all_req = Access.objects.all().order_by('-create_date')
    request_for_accept = List_of_Accept.objects.filter(
        Access_ID__approve_list__user_boss__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_boss="Ожидание").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(
        Access_ID__approve_list__user_boss__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_boss="Ожидание согласования").values("Access_ID").distinct() \
                         | List_of_Accept.objects.filter(
        Access_ID__approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name).values(
        "Access_ID").distinct() \
                         | List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).exclude(
        Accepter_Status="Ожидание").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).exclude(
        Accepter_Status="Ожидание согласования").values("Access_ID").distinct()

    requests = Access.objects.filter(
        approve_list__user_boss__contains=request.user.userprofile.user_full_name) | Access.objects.filter(
        approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name)
    boss_requests = ApproveList.objects.filter(
        user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
    service_requests = List_of_Accept.objects.all()
    accepter_services = List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).values(
        "Access_ID").distinct()
    approve_request = ApproveList.objects.all()
    context = {
        'request_for_accept': request_for_accept,
        'all_req': all_req,
        'accepter_services': accepter_services,
        'requests': requests,
        'approve_request': approve_request,
        'boss_requests ': boss_requests,
        'service_requests': service_requests
    }
    return render(request, 'request_access/request_actions.html', context)


@login_required
def request_actions(request):
    all_req = Access.objects.all().order_by('-create_date')
    request_for_accept = List_of_Accept.objects.filter(
        Access_ID__approve_list__user_boss__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_boss="Согласовано").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(
        Access_ID__approve_list__user_boss__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_boss="Не согласовано").values("Access_ID").distinct() \
                         | List_of_Accept.objects.filter(
        Access_ID__approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_ib="Согласовано").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(
        Access_ID__approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_ib="Не согласовано").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(
        Access_ID__approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name).exclude(
        Access_ID__approve_list__approve_status_ib="Ожидание").values("Access_ID").distinct() \
                         | List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).exclude(
        Accepter_Status="Согласовано").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).exclude(
        Accepter_Status="Не согласовано").values("Access_ID").distinct() \
                         & List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).exclude(
        Accepter_Status="Ожидание").values("Access_ID").distinct()

    requests = Access.objects.filter(
        approve_list__user_boss__contains=request.user.userprofile.user_full_name) | Access.objects.filter(
        approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name)
    boss_requests = ApproveList.objects.filter(
        user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
    service_requests = List_of_Accept.objects.all()
    accepter_services = List_of_Accept.objects.filter(Accepter_FIO=request.user.userprofile.user_full_name).values(
        "Access_ID").distinct()
    approve_request = ApproveList.objects.all()
    context = {
        'request_for_accept': request_for_accept,
        'all_req': all_req,
        'accepter_services': accepter_services,
        'requests': requests,
        'approve_request': approve_request,
        'boss_requests ': boss_requests,
        'service_requests': service_requests
    }
    return render(request, 'request_access/request_actions.html', context)


@login_required
def RequestActionDetail(request, id):
    approver = ApproveChanger()
    get_request = Access.objects.get(id=id)
    user_requests = Access.objects.filter(author=request.user)
    services_request = List_of_Accept.objects.filter(Access_ID=id)
    access_checker = False
    access_company = Access.objects.get(id=id).author.userprofile.user_company
    # Чекаем размещение комментов
    checker_comments = checker_services(id)
    checker_approve = checker_approve_list(id)
    print(checker_comments)
    print(checker_approve)
    for accepter in services_request:
        print(f'{accepter.Accepter_FIO} = {request.user.userprofile.user_full_name}')
        if accepter.Accepter_FIO == request.user.userprofile.user_full_name:
            access_checker = True
        else:
            pass
    print(f'{access_checker} = {request.user.userprofile.user_full_name}')
    if ApproveList.objects.filter(user_boss='Чаленко Анатолий Юрьевич'):
        context = {
            'access_checker': access_checker,
            'approver': approver,
            'get_request': get_request,
            'user_requests': user_requests,
            'services_request': services_request,
            'checker_comments': checker_comments,
            'checker_approve': checker_approve,
            'access_company': access_company
        }
    else:
        boss_requests = ApproveList.objects.filter(
            user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
        context = {
            'access_checker': access_checker,
            'approver': approver,
            'get_request': get_request,
            'user_requests': user_requests,
            'services_request': services_request,
            'boss_requests': boss_requests,
            'checker_comments': checker_comments,
            'checker_approve': checker_approve,
            'access_company': access_company
        }
    template = 'request_access/request_detail.html'
    print(request.method)
    if request.method == 'POST':
        print("Проверка отправки комментария")
        print(request.POST)
        if 'modal_comment_btn' in request.POST:
            main_access_task = Access.objects.get(id=id)
            print("Отправка комментариев")
            comment = request.user.userprofile.user_full_name + ": " + request.POST['comment_text'] + "\n"
            print(f"Номер заявки {id}")
            main_access_task.comments += comment
            main_access_task.save(update_fields=["comments"])
            return HttpResponseRedirect(reverse('request_detail', kwargs={'id': id}))
        else:
            print(f"Номер заявки {id}")
            main_access_task = Access.objects.get(id=id)
            task = Access.objects.get(id=id).approve_list
            all_services_on_task = List_of_Accept.objects.filter(Access_ID=id)
            service_approve = List_of_Accept.objects.filter(Access_ID=id) & List_of_Accept.objects.filter(
                Accepter_FIO=request.user.userprofile.user_full_name)
            print(f" Пользователь {request.user.userprofile.user_full_name}")
            if request.user.userprofile.user_full_name == task.user_boss and task.approve_status_boss != "Согласовано":
                print(f"{task.user_boss} BOSS")
                task.approve_status_boss = request.POST.get('approve_choicer')
                if request.POST.get('approve_choicer') == "Не согласовано":
                    # task.approve_status_owner = request.POST.get('approve_choicer')
                    for service in all_services_on_task:
                        service.Accepter_Status = request.POST.get('approve_choicer')
                        service.save(update_fields=["Accepter_Status"])
                    task.approve_status_ib = request.POST.get('approve_choicer')
                    main_access_task.request_statuser = "Не согласовано руководителем"
                    task.save(update_fields=["approve_status_boss", "approve_status_ib"])
                    main_access_task.save(update_fields=["request_statuser"])
                else:
                    for service in all_services_on_task:
                        service.Accepter_Status = "Ожидание согласования"
                        service.save(update_fields=["Accepter_Status"])
                    task.approve_status_ib = "Ожидание"
                    main_access_task.request_statuser = "Ожидание согласования сервисов"
                    task.save(update_fields=["approve_status_boss", "approve_status_ib"])
                    main_access_task.save(update_fields=["request_statuser"])
            elif request.user.userprofile.user_full_name != task.ib_spec.specialist_ib.userprofile.user_full_name:
                for service in service_approve:
                    if service.Accepter_FIO == request.user.userprofile.user_full_name:
                        print(request.POST.get(f"ACCEPTED_{service.Accepted_Service.service_name}"))
                        print(f"ID = {service.id}")
                        if service.Accepted_Service.service_name == request.POST.get(
                                f"ACCEPTED_{service.Accepted_Service.service_name}"):
                            if request.user.userprofile.user_full_name == service.Accepter_FIO:
                                print("Пытаемся согласовать сервис")
                                print("СОГЛАСОВЫВАЕМ")
                                print(f"{service.Accepted_Service.service_name} SERVICE")
                                service.Accepter_Status = "Согласовано"
                                service.save(update_fields=["Accepter_Status"])
                            else:
                                # main_access_task.request_statuser = "Ожидание согласования отдела ИБ"
                                # service_approve.save(update_fields=["Accepter_Status"])
                                print("Что то пошло не так")
                                # main_access_task.save(update_fields=["request_statuser"])
                        if service.Accepted_Service.service_name == request.POST.get(
                                f"DECLINED_{service.Accepted_Service.service_name}"):
                            if request.user.userprofile.user_full_name == service.Accepter_FIO:
                                print("ОТБОЙ")
                                print(f"{service.Accepted_Service.service_name} SERVICE")
                                service.Accepter_Status = "Не согласовано"
                                service.save(update_fields=["Accepter_Status"])
                            else:
                                print("Что то пошло не так")
                count_services = all_services_on_task.count()
                accepted = 0
                declined = 0
                for serv in all_services_on_task:
                    if serv.Accepter_Status == "Согласовано":
                        accepted += 1
                    if serv.Accepter_Status == "Не согласовано":
                        declined += 1
                print(f"Согласовано сервисов {accepted} из {count_services}")
                print(f"Несогласовано сервисов: {declined} из {count_services}")
                if accepted + declined == count_services and declined == count_services:
                    print("Круг согласования сервисов завершен, отмена заявки")
                    task.approve_status_ib = "Не согласовано"
                    task.save(update_fields=["approve_status_ib"])
                    main_access_task.request_statuser = "Не согласовано ответсветнными за Сервис"
                    main_access_task.save(update_fields=["request_statuser"])
                elif accepted + declined == count_services and declined != count_services or accepted == count_services:
                    print("Круг согласования сервисов завершен, передача в ИБ")
                    task.approve_status_ib = "Ожидание согласования"
                    task.save(update_fields=["approve_status_ib"])
                    main_access_task.request_statuser = "Ожидание согласования ИБ"
                    main_access_task.save(update_fields=["request_statuser"])
                else:
                    print("Круг согласования сервисов не завершен.")
            else:
                if request.user.userprofile.user_full_name == task.ib_spec.specialist_ib.userprofile.user_full_name:
                    main_access_task.request_statuser = request.POST.get('approve_choicer')
                    task.approve_status_ib = request.POST.get('approve_choicer')
                    if request.POST.get('approve_choicer') == "Не согласовано":
                        task.approve_status_boss = request.POST.get('approve_choicer')
                        for service in all_services_on_task:
                            service.Accepter_Status = request.POST.get('approve_choicer')
                            service.save(update_fields=["Accepter_Status"])
                        main_access_task.request_statuser = "Не согласовано отделом ИБ"
                        task.save(update_fields=["approve_status_boss", "approve_status_ib"])
                        main_access_task.save(update_fields=["request_statuser"])
                    else:
                        task.approve_status_ib = "Согласовано"
                        task.save(update_fields=["approve_status_ib"])
                        main_access_task.request_statuser = "Заявка согласована"
                        main_access_task.save(update_fields=["request_statuser"])
                # return render(request, template, context)
            return HttpResponseRedirect(reverse('request_detail', kwargs={'id': id}))
    else:
        return render(request, template, context)


# Проектная модель множественного выбора сервисов.
@login_required()
def m_access(request):
    if (request.user.userprofile.user_company.company_activator == True):
        template = 'request_access/m_access.html'
        name_pc = platform.node()
        if request.method == 'POST':
            form_mn = AccessForm(request.POST)
            form_cs = AccepterForm(request.POST)
            form_ap = ApproveForm(request.POST)
            if form_cs.is_valid() and form_mn.is_valid() and form_ap.is_valid():  # and form_cs.is_valid():
                model_ap = form_ap.save(commit=False)
                if request.POST.get('outer_user', False):
                    outer = request.POST['outer_user']
                    print(f'Внешний триггер установлен {outer} обработка заявки для внешнего пользователя начата:')
                else:
                    print('Триггер не установлен обработка заявки как обычной заявки')
                if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
                    creator_boss = User.objects.filter(userprofile__user_full_name=request.POST.get('user_name'))
                    for boss in creator_boss:
                        if boss == request.user:
                            checked_boss = boss.userprofile.user_boss.userprofile.user_full_name
                            checked_boss_email = boss.userprofile.user_boss.userprofile.user_email
                            model_ap.user_boss = checked_boss
                            model_ap.email_boss = checked_boss_email
                        print(f"Выводим тестовый параметр{request.user} и его босс {boss}")
                else:
                    model_ap.user_boss = request.user.userprofile.user_boss.userprofile.user_full_name
                    model_ap.email_boss = request.user.userprofile.user_boss.userprofile.user_email
                model_ap.save()
                model_mn = form_mn.save(commit=False)
                if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
                    checker_author = User.objects.filter(userprofile__user_full_name=request.POST.get('user_name'))
                    for author in checker_author:
                        if author == request.user:
                            model_mn.author = User.objects.get(userprofile__user_full_name=author.userprofile.user_boss.userprofile.user_full_name)
                else:
                    model_mn.author = request.user
                model_mn.creator = request.user
                model_mn.approve_list = model_ap
                model_mn.save()
                context = {
                    "created_task": model_mn
                }
                print(f"{form_cs.cleaned_data['Cool_Story']} Получили вот что")

                for pickers in form_cs.cleaned_data['Cool_Story']:
                    print(f"Пошла {pickers}")
                    service = Service.objects.get(id=pickers)
                    print("Номер заявки" + str(request.POST.get('Access_ID')))
                    print("Выудили сервис " + str(service.service_name))
                    print(service.service_group.group_sowner.userprofile.user_full_name)
                    print(service.service_group.group_sowner.userprofile.user_email)
                    print("============================================")
                    model_cs = form_cs.save(commit=False)
                    print(model_mn.id)
                    model_cs.Access_ID = model_mn
                    model_cs.Accepter_FIO = service.service_group.group_sowner.userprofile.user_full_name
                    model_cs.Accepted_Service = service
                    model_cs.Email_Accepter = service.service_group.group_sowner.userprofile.user_email
                    model_cs.pk = None
                    model_cs.save()
                model_mn = AccessForm()
                model_cs = AccepterForm()
                model_ap = ApproveForm()

                return render(request, 'request_access/test_inline.html', context)
                # return HttpResponseRedirect(reverse('created_task', kwargs={'id': id}))
            else:
                print("Не Пошла!")
        # Обработка GET запроса для внутренних и внешних пользователей.
        services_bd = Service.objects.all()
        # Инициализация формы Форма Согласования
        form_approve = AccepterForm()
        # Инициализация формы Отправки письма.
        form_sendmail = EmailForm(
            initial={'email': request.user.userprofile.user_email, 'subject': f"Запрос на доступ №{id}",
                     'message': '1'})
        form_request = AccessForm(initial={
            'user_name': request.user.userprofile.user_full_name,
            'user_dep': request.user.userprofile.user_dep,
            'user_otdel': request.user.userprofile.user_otdel,
            'approve_list': ApproveList.objects.get(id=60)
        })
        form_bosslist = ApproveForm(
            initial={
                'email_ib': InformationSecurity.objects.get(active=True).specialist_ib_email,
                'number_task': '',
                'ib_spec': InformationSecurity.objects.get(active=True),
                'user_boss': request.user.userprofile.user_boss.userprofile.user_full_name,
                'email_boss': request.user.userprofile.user_boss.userprofile.user_email,
                'change_date': datetime.now(),
            }
        )
        advanced_form = Additional_Service()
        file_deps = File_Deps_Form()
        outer_users = UserProfile.objects.exclude(user_company=1)
        context = {
            'outer_users': outer_users,
            'name_pc': name_pc,
            'form_approve': form_approve,
            'form_sendmail': form_sendmail,
            'form_request': form_request,
            'form_bosslist': form_bosslist,
            'services_bd': services_bd,
            'rangered': range(2),
            'advanced_form': advanced_form,
            'file_deps': file_deps
        }
        return render(request, template, context)
    else:
        template = 'request_access/outer_access.html'
        name_pc = platform.node()
        if request.method == 'POST':
            form_mn = AccessForm(request.POST)
            form_cs = AccepterForm(request.POST)
            form_ap = ApproveForm(request.POST)
            if form_cs.is_valid() and form_mn.is_valid() and form_ap.is_valid():  # and form_cs.is_valid():
                model_ap = form_ap.save(commit=False)
                model_ap.user_boss = 'Чаленко Анатолий Юрьевич'
                model_ap.email_boss = 'chalenko_ay@rusagrotrans.ru'
                # model_ap.approve_status_boss = "Согласовано"
                model_ap.save()
                model_mn = form_mn.save(commit=False)
                if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
                    model_mn.author = User.objects.get(userprofile__user_full_name=request.POST.get('user_name'))
                else:
                    model_mn.author = request.user
                model_mn.creator = request.user
                model_mn.approve_list = model_ap
                model_mn.save()
                context = {
                    "created_task": model_mn
                }
                print(f"{form_cs.cleaned_data['Cool_Story']} Получили вот что")

                for pickers in form_cs.cleaned_data['Cool_Story']:
                    print(f"Пошла {pickers}")
                    service = Service.objects.get(id=pickers)
                    print("Номер заявки" + str(request.POST.get('Access_ID')))
                    print("Выудили сервис " + str(service.service_name))
                    print(service.service_group.group_sowner.userprofile.user_full_name)
                    print(service.service_group.group_sowner.userprofile.user_email)
                    print("============================================")
                    model_cs = form_cs.save(commit=False)
                    print(model_mn.id)
                    model_cs.Access_ID = model_mn
                    model_cs.Accepter_FIO = service.service_group.group_sowner.userprofile.user_full_name
                    model_cs.Accepted_Service = service
                    model_cs.Accepter_Status = "Ожидание согласования"
                    model_cs.Email_Accepter = service.service_group.group_sowner.userprofile.user_email
                    model_cs.pk = None
                    model_cs.save()
                model_mn = AccessForm()
                model_cs = AccepterForm()
                model_ap = ApproveForm()

                return render(request, 'request_access/test_inline.html', context)
                # return HttpResponseRedirect(reverse('created_task', kwargs={'id': id}))
            else:
                print("Не Пошла!")

            context = {}
        # Обработка GET запроса
        else:
            # Загрузка данных по сервисам
            services_bd = Service.objects.all()
            # Инициализация формы Форма Согласования
            form_approve = AccepterForm()
            # Инициализация формы Отправки письма.
            form_sendmail = EmailForm(
                initial={'email': request.user.userprofile.user_email, 'subject': "Запрос на доступ №", 'message': '1'})
            # Инициализация формы создания запроса, начальными данными
            form_request = Outer_Access_Form(initial={
                'user_name': request.user.userprofile.user_full_name,
                'user_dep': request.user.userprofile.user_dep,
                'user_otdel': request.user.userprofile.user_otdel,
                'approve_list': ApproveList.objects.get(id=60),
                'user_company': request.user.userprofile.user_company,
                'user_position': request.user.userprofile.user_position
            })
            # Инициализация листа согласования для внешних пользователей.
            form_bosslist = ApproveForm(
                initial={
                    'email_ib': InformationSecurity.objects.get(active=True).specialist_ib_email,
                    'number_task': '',
                    'ib_spec': InformationSecurity.objects.get(active=True),
                    # 'user_boss': request.user.userprofile.user_boss.userprofile.user_full_name,
                    # 'email_boss': request.user.userprofile.user_boss.userprofile.user_email,
                    'change_date': datetime.now(),
                }
            )
            advanced_form = Additional_Service()
            file_deps = File_Deps_Form()
            context = {
                'name_pc': name_pc,
                'form_approve': form_approve,
                'form_sendmail': form_sendmail,
                'form_request': form_request,
                'form_bosslist': form_bosslist,
                'services_bd': services_bd,
                'rangered': range(2),
                'advanced_form': advanced_form,
                'file_deps': file_deps
            }
            return render(request, template, context)


# Представление Главной страницы оформления заявки на доступ.
@login_required()
def index(request):
    template = 'request_access/access.html'
    if request.method == 'POST':
        form_mn = AccessForm(request.POST)
        form_cs = ApproveForm(request.POST)
        if form_mn.is_valid() and form_cs.is_valid():
            model_cs = form_cs.save(commit=False)
            model_cs.user_boss = UserProfile.objects.get(
                user_full_name=request.POST.get('user_name')).user_boss.userprofile.user_full_name
            model_cs.email_boss = UserProfile.objects.get(
                user_full_name=request.POST.get('user_name')).user_boss.userprofile.user_email
            print(model_cs.user_boss)
            print(model_cs)
            model_cs.save()
            model_mn = form_mn.save(commit=False)
            if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
                model_mn.author = User.objects.get(userprofile__user_full_name=request.POST.get('user_name'))
            else:
                model_mn.author = request.user
            model_mn.creator = request.user
            model_mn.approve_list = model_cs
            model_mn.save()
            context = {
                "created_task": model_mn
            }
            model_mn = AccessForm()
            model_cs = ApproveForm()
            return render(request, 'request_access/test_inline.html', context)
            # Form2
    services_bd = Service.objects.all()
    # Инициализация формы Форма Согласования
    form_approve = ApproveForm(
        initial={
            'email_service_owner': Service.objects.get(id=1).service_owner.user_email,
            'email_ib': InformationSecurity.objects.get(active=True).specialist_ib_email,
            'number_task': '',
            'ib_spec': InformationSecurity.objects.get(id=1),
            'user_boss': request.user.userprofile.user_boss.userprofile.user_full_name,
            'service_owner': 'Чаленко Анатолий Юрьевич',
            'change_date': datetime.now(),
            'fileserver_owner': "",

        }
    )
    # Инициализация формы Отправки письма.
    form_sendmail = EmailForm(
        initial={'email': request.user.userprofile.user_email, 'subject': "Запрос на доступ №", 'message': '1'})
    form_request = AccessForm(initial={
        'user_name': request.user.userprofile.user_full_name,
        'user_dep': request.user.userprofile.user_dep,
        'user_otdel': request.user.userprofile.user_otdel,
        'approve_list': ApproveList.objects.get(id=60)
    })
    context = {
        'form_approve': form_approve,
        'form_sendmail': form_sendmail,
        'form_request': form_request,
        'services_bd': services_bd
    }
    return render(request, template, context)


@login_required
def email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = datetime.now()
            post.save()
            email = request.POST.get('email')
            subject = str(request.POST.get('subject')) + " " + str(post.id)
            message = request.POST.get('message')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.send()
            return render(request, 'Main_templates/index.html')
    else:
        form = EmailForm()
    return render(request, 'request_access/sendmail.html', {'form': form})


# Раздел страницы менеджера для создания внешних пользователей и добавления компаний.
def manager_page(request):
    companys = Companys.objects.all()
    form_user = UserForm()
    form_userprofile = UserProfileForm()
    company_form = CompanyRegister()
    outer_user = UserProfile.objects.exclude(user_company=1)
    context = {
        'companys': companys,
        'form_user': form_user,
        'company_form': company_form,
        'outer_user': outer_user,
        'form_userprofile': form_userprofile,

    }
    if request.method == 'POST':
        if 'modal_company_btn' in request.POST:
            model_company = CompanyRegister(request.POST)
            if model_company.is_valid:
                print("Сохраняем компанию")
                model_company.save()
            return HttpResponseRedirect(reverse('manager'))
    return render(request, 'request_access/manager_page.html', context)


# @login_required
# def created_task(request, id):
#    created_task = id
#    return render(request, 'request_access/test_inline.html', {'created_task': created_task})

# Проерка согласования сервисов
def checker_services(id):
    all_services_on_task = List_of_Accept.objects.filter(Access_ID=id)
    count_services = all_services_on_task.count()
    accepted = 0
    declined = 0
    for serv in all_services_on_task:
        if serv.Accepter_Status == "Согласовано":
            accepted += 1
        if serv.Accepter_Status == "Не согласовано":
            declined += 1
    if accepted + declined == count_services and declined == count_services:
        # print("Круг согласования сервисов завершен, отмена заявки")
        checker_comments = True
    elif accepted + declined == count_services and declined != count_services or accepted == count_services:
        # print("Круг согласования сервисов завершен, передача в ИБ")
        checker_comments = True
    else:
        # print("Круг согласования сервисов не завершен.")
        checker_comments = False
    return checker_comments


def checker_approve_list(id):
    approve_list = Access.objects.get(id=id).approve_list
    if (approve_list.approve_status_ib == "Согласовано" or approve_list.approve_status_ib == "Не согласовано") and (
            approve_list.approve_status_boss == "Согласовано" or approve_list.approve_status_boss == "Не согласовано"):
        checker_approve = True
    else:
        checker_approve = False
    return checker_approve
