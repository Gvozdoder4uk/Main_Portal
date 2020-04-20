from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import *


def index(request):
    services_bd = Service.objects.all()
    last_request = Access.objects.all().last()
    form_request = AccessForm(initial={
        'name_user': request.user.userprofile.user_last_name + " " + request.user.userprofile.user_first_name + " " + request.user.userprofile.user_second_name,
        'user_dep': request.user.userprofile.user_dep,
        'user_otdel': request.user.userprofile.user_otdel,
        'user_boss': request.user.userprofile.user_boss,
        'user_dep': request.user.userprofile.user_dep,
        'service_owner': 'Чаленко Анатолий Юрьевич',
        'ib_spec': "Кривощеков Николай Сергеевич"
    })
    template = 'request_access/access.html'
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form_request': form_request,
        'last_request': last_request,
        'services_bd': services_bd
    }
    return render(request, template, context)


@login_required
def cabinet(request):
    return render(request, 'request_access/cabinet.html')


def personal_cabinet(request):
    user_requests = Access.objects.filter(name_user__contains=request.user.userprofile.user_last_name)
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
