from django.shortcuts import render
from .models import *


# Create your views here.


def index(request):
    return render(request, 'inventory/index.html')


def access(request):
    return render(request, 'inventory/access.html')


def index(request):
    firstname = Ad_users.objects.all().count()
    secondname = Ad_users.objects.all().count()
    lastname = Ad_users.objects.all().count()
    num_authors = Ad_users.objects.all().count()

    return render(request, 'index.html', context={'книжули': num_books, 'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors})
