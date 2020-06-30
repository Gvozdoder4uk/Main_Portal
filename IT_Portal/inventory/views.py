from django.shortcuts import render
from .models import *


# Create your views here.


def index(request):
    return render(request, 'inventory/index.html')


def access(request):
    return render(request, 'inventory/index.html')


def portal_test(request):
    return render(request, 'inventory/portal_test.html')