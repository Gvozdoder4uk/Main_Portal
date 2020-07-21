from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from IT_Portal import settings
from datetime import *
import platform
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import time


def is_member(user):
    return user.groups.filter(name='Admin Reestr').exists()


@login_required
def cabinet(request):
    if request.user.groups.filter(name='Admin Reestr').exists():
        service_requests = List_of_Accept.objects.all()
        all_requests = Access.objects.all().order_by('-create_date')
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
        Access_ID__approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name).values(
        "Access_ID").distinct() \
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
    boss_requests = ApproveList.objects.filter(
        user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
    context = {
        'approver': approver,
        'get_request': get_request,
        'user_requests': user_requests,
        'services_request': services_request,
        'boss_requests': boss_requests,
    }
    template = 'request_access/request_detail.html'
    if request.method == 'POST':
        print(f"Номер заявки {id}")
        main_access_task = Access.objects.get(id=id)
        task = Access.objects.get(id=id).approve_list
        all_services_on_task = List_of_Accept.objects.filter(Access_ID=id)
        service_approve = List_of_Accept.objects.filter(Access_ID=id) & List_of_Accept.objects.filter(
            Accepter_FIO=request.user.userprofile.user_full_name)
        print(f" Пользователь {request.user.userprofile.user_full_name}")
<<<<<<< HEAD
        if request.user.userprofile.user_full_name == task.user_boss and task.approve_status_boss != "Согласовано":
=======
        if request.user.userprofile.user_full_name == task.user_boss and task.approve_status_boss!="Согласовано":
>>>>>>> master
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
                            # main_access_task.save(update_fields=["request_statuser"])'''
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
                main_access_task.request_statuser = "Не согласовано"
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
                    # task.approve_status_owner = request.POST.get('approve_choicer')
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

    return render(request, template, context)


from django.core.files.storage import FileSystemStorage
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage


# Проектная модель множественного выбора сервисов.
@login_required()
def m_access(request):
    template = 'request_access/m_access.html'
    name_pc = platform.node()
    if request.method == 'POST':
        form_mn = AccessForm(request.POST)
        form_cs = AccepterForm(request.POST)
        form_ap = ApproveForm(request.POST)
        if form_cs.is_valid() and form_mn.is_valid() and form_ap.is_valid():  # and form_cs.is_valid():
            model_ap = form_ap.save(commit=False)
            if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
                creator_boss = User.objects.get(userprofile__user_full_name=request.POST.get('user_name'))
                model_ap.user_boss = creator_boss.userprofile.user_boss.userprofile.user_full_name
                model_ap.email_boss = creator_boss.userprofile.user_boss.userprofile.user_email
            else:
                model_ap.user_boss = request.user.userprofile.user_boss.userprofile.user_full_name
                model_ap.email_boss = request.user.userprofile.user_boss.userprofile.user_email
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
                model_cs.Email_Accepter = service.service_group.group_sowner.userprofile.user_email
                model_cs.pk = None
                model_cs.save()
            model_mn = AccessForm()
            model_cs = AccepterForm()
            model_ap = ApproveForm()

            return render(request, 'request_access/test_inline.html', context)
            #return HttpResponseRedirect(reverse('created_task', kwargs={'id': id}))
        else:
            print("Не Пошла!")

        context = {}

        # Form2
    services_bd = Service.objects.all()
    # Инициализация формы Форма Согласования
    form_approve = AccepterForm(

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


#@login_required
#def created_task(request, id):
#    created_task = id
#    return render(request, 'request_access/test_inline.html', {'created_task': created_task})
