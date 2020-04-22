from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import *
from IT_Portal import settings
from datetime import *
from django.forms.models import inlineformset_factory
from django.db.models import Q

@login_required
def cabinet(request):
    return render(request, 'request_access/cabinet.html')


def personal_cabinet(request):
    user_requests = Access.objects.filter(name_user__contains=request.user.userprofile.user_last_name) | Access.objects.filter(name_user__contains=request.user.userprofile.user_last_name)
    context = {
        'user_requests': user_requests,
    }
    return render(request, 'request_access/personal_request.html', context)


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


def request_actions(request):

    user_requests = ApproveList.objects.filter(service_owner__contains=request.user.userprofile.user_last_name)
    requests = Access.objects.filter(approve_list__service_owner__contains=request.user.userprofile.user_last_name)
    boss_requests = ApproveList.objects.filter(user_boss__contains=request.user.userprofile.user_boss)
    approve_request = ApproveList.objects.all()
    context = {
        'requests':requests,
        'approve_request': approve_request,
        'user_requests': user_requests,
        'boss_requests ': boss_requests
    }
    return render(request, 'request_access/request_actions.html', context)


def RequestActionDetail(request, id):
    get_request = Access.objects.get(id=id)
    user_requests = Access.objects.filter(name_user__contains=request.user.userprofile.user_last_name)
    owner_requests = ApproveList.objects.filter(service_owner__contains=request.user.userprofile.user_last_name)
    boss_requests = ApproveList.objects.filter(user_boss__contains=request.user.userprofile.user_boss)
    context = {
        'get_request': get_request,
        'user_requests': user_requests,
        'owner_requests': owner_requests,
        'boss_requests': boss_requests,
    }
    template = 'request_access/request_detail.html'
    return render(request, template, context)


from django.core.files.storage import FileSystemStorage
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage


@login_required()
def index(request):
    template = 'request_access/access.html'
    if request.method == 'POST':
        form_mn = AccessForm(request.POST)
        form_cs = ApproveForm(request.POST)
        if form_mn.is_valid() and form_cs.is_valid():
            model_cs = form_cs.save()
            print(model_cs)
            model_mn = form_mn.save(commit=False)
            model_mn.approve_list = model_cs
            model_mn.save()
            return render(request, 'request_access/test_inline.html')
            # Form2
    services_bd = Service.objects.all()
    form_approve = ApproveForm(
        initial={
            'email_service_owner': Service.objects.get(id=1).service_owner.user_email,

            'email_ib': InformationSecurity.objects.get(active=True).specialist_ib_email,
            'number_task': '',
            'ib_spec': InformationSecurity.objects.get(id=1),
            'user_boss': request.user.userprofile.user_boss,
            'service_owner': 'Чаленко Анатолий Юрьевич',
            'change_date': datetime.now(),
            'fileserver_owner': "",


        }
    )
    form_sendmail = EmailForm(
        initial={'email': request.user.userprofile.user_email, 'subject': "Запрос на доступ №", 'message': '1'})
    form_request = AccessForm(initial={
        'name_user': request.user.userprofile.user_last_name + " " + request.user.userprofile.user_first_name + " " + request.user.userprofile.user_second_name,
        'user_dep': request.user.userprofile.user_dep,
        'user_otdel': request.user.userprofile.user_otdel,
        'approve_list': ApproveList.objects.get(id=1)
    })
    context = {
        'form_approve': form_approve,
        'form_sendmail': form_sendmail,
        'form_request': form_request,
        'services_bd': services_bd
    }
    return render(request, template, context)


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
