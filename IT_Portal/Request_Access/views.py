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
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import get_messages


def is_member(user):
    return user.groups.filter(name='Admin Reestr').exists()


@login_required
def cabinet(request):
    if request.user.groups.filter(name='Admin Reestr').exists():
        all_requests = Access.objects.all().order_by('-create_date')
        context = {
            'all_requests': all_requests
        }
        return render(request, 'request_access/cabinet.html', context)
    else:
        return render(request, 'Main_templates/404.html')


@login_required
def personal_cabinet(request):
    user_requests = Access.objects.filter(author=request.user)
    context = {
        'user_requests': user_requests,
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


def edit_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()

    list_requests = Requests.objects.all()
    form = RequestForm()
    context = {
        'list_requests': list_requests,
        'form': form
    }
    template = 'request_access/edit_request.html'
    return render(request, template, context)


@login_required
def request_actions(request):
    requests = Access.objects.filter(
        approve_list__service_owner__contains=request.user.userprofile.user_last_name) | Access.objects.filter(
        approve_list__user_boss__contains=request.user.userprofile.user_full_name) | Access.objects.filter(
        approve_list__ib_spec__specialist_ib__userprofile__user_full_name__contains=request.user.userprofile.user_full_name)
    boss_requests = ApproveList.objects.filter(
        user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
    approve_request = ApproveList.objects.all()
    context = {
        'requests': requests,
        'approve_request': approve_request,
        'boss_requests ': boss_requests
    }
    return render(request, 'request_access/request_actions.html', context)


@login_required
def RequestActionDetail(request, id):
    approver = ApproveChanger()
    get_request = Access.objects.get(id=id)
    user_requests = Access.objects.filter(author=request.user)
    owner_requests = ApproveList.objects.filter(service_owner__contains=request.user.userprofile.user_last_name)
    boss_requests = ApproveList.objects.filter(
        user_boss__contains=request.user.userprofile.user_boss.userprofile.user_full_name)
    context = {
        'approver': approver,
        'get_request': get_request,
        'user_requests': user_requests,
        'owner_requests': owner_requests,
        'boss_requests': boss_requests,
    }
    template = 'request_access/request_detail.html'
    if request.method == 'POST':
        main_access_task = Access.objects.get(id=id)
        task = Access.objects.get(id=id).approve_list
        print(task)
        print(request.user.userprofile.user_full_name)
        if request.user.userprofile.user_full_name == task.user_boss:
            print(f"{task.user_boss} BOSS")
            task.approve_status_boss = request.POST.get('approve_choicer')
            if request.POST.get('approve_choicer') == "Не согласовано":
                task.approve_status_owner = request.POST.get('approve_choicer')
                task.approve_status_ib = request.POST.get('approve_choicer')
                main_access_task.request_statuser = "Не согласовано руководителем"
                task.save(update_fields=["approve_status_boss", "approve_status_owner", "approve_status_ib"])
                main_access_task.save(update_fields=["request_statuser"])
            else:
                task.approve_status_owner = "Ожидание согласования"
                task.approve_status_ib = "Ожидание согласования"
                main_access_task.request_statuser = "Ожидание согласования Владельца Сервиса и ИБ"
                task.save(update_fields=["approve_status_boss", "approve_status_owner", "approve_status_ib"])
                main_access_task.save(update_fields=["request_statuser"])
        if request.user.userprofile.user_full_name == task.service_owner:
            print(f"{task.service_owner} SERVICE")
            task.approve_status_owner = request.POST.get('approve_choicer')
            if request.POST.get('approve_choicer') == "Не согласовано":
                task.approve_status_boss = request.POST.get('approve_choicer')
                task.approve_status_ib = request.POST.get('approve_choicer')
                main_access_task.request_statuser = "Не согласовано владельцем сервиса"
                task.save(update_fields=["approve_status_boss", "approve_status_owner", "approve_status_ib"])
                main_access_task.save(update_fields=["request_statuser"])
            else:
                main_access_task.request_statuser = "Ожидание согласования отдела ИБ"
                task.save(update_fields=["approve_status_owner"])
                main_access_task.save(update_fields=["request_statuser"])
        if request.user.userprofile.user_full_name == task.ib_spec.specialist_ib.userprofile.user_full_name:
            main_access_task.request_statuser = request.POST.get('approve_choicer')
            task.approve_status_ib = request.POST.get('approve_choicer')
            if request.POST.get('approve_choicer') == "Не согласовано":
                task.approve_status_boss = request.POST.get('approve_choicer')
                task.approve_status_owner = request.POST.get('approve_choicer')
                main_access_task.request_statuser = "Не согласовано отделом ИБ"
                task.save(update_fields=["approve_status_boss", "approve_status_owner", "approve_status_ib"])
                main_access_task.save(update_fields=["request_statuser"])
            else:
                task.save(update_fields=["approve_status_ib"])
                main_access_task.request_statuser = "Заявка согласована"
                main_access_task.save(update_fields=["request_statuser"])
        return render(request, template, context)

    return render(request, template, context)


from django.core.files.storage import FileSystemStorage
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage


# Проектная модель множественного выбора сервисов.
@login_required()
def m_access(request):
    template = 'request_access/m_access.html'
    if request.method == 'POST':
        # form_mn = AccessForm(request.POST)
        form_cs = AccepterForm(request.POST)
        if form_cs.is_valid():  # and form_cs.is_valid():
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
                model_cs.Access_ID = Access.objects.get(id=request.POST.get('Access_ID'))
                model_cs.Accepter_FIO = service.service_group.group_sowner.userprofile.user_full_name
                model_cs.Accepted_Service = service
                model_cs.Email_Accepter = service.service_group.group_sowner.userprofile.user_email
                model_cs.pk = None
                model_cs.save()
                #return render(request, 'request_access/m_access.html')
        else:
            print("Не Пошла!")
            # model_cs = form_cs.save(commit=False)
            # model_cs.user_boss = UserProfile.objects.get(
            #    user_full_name=request.POST.get('user_name')).user_boss.userprofile.user_full_name
            # model_cs.email_boss = UserProfile.objects.get(
            #    user_full_name=request.POST.get('user_name')).user_boss.userprofile.user_email
            # print(model_cs.user_boss)
            # print(model_cs)
            # model_cs.save()
            # model_mn = form_mn.save(commit=False)
            # if User.objects.filter(userprofile__user_full_name=request.POST.get('user_name')).exists():
            #    model_mn.author = User.objects.get(userprofile__user_full_name=request.POST.get('user_name'))
            # else:
            #    model_mn.author = request.user
            # model_mn.creator = request.user
            # model_mn.approve_list = model_cs
            # model_mn.save()
            #    "created_task": model_mn
            # }
            model_mn = AccessForm()
            model_cs = ApproveForm()
        context = {}
        return render(request, 'request_access/m_access.html')
            # Form2
    services_bd = Service.objects.all()
    # Инициализация формы Форма Согласования
    form_approve = AccepterForm()
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

# @login_required
# def created_task(request):
#   return render(request, 'request_access/test_inline.html', {"created_task": saved_data})
