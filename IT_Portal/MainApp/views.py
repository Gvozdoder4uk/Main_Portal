from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from Request_Access.models import *


# Create your views here.
def index(request):
    req_count = Access.objects.all().count
    context = {
        'req_count': req_count
    }
    return render(request, 'Main_Templates/index.html', context)


def daynight(request):
    return render(request, 'Main_Templates/DayNight.html')


def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'MainApp/profile.html', {"query": query})
    else:
        return render(request, 'app_foldername/login.html', {})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        post = User.objects.filter(username=username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/#about")
        else:
            return render(request, 'Main_Templates/login.html', {})
    return render(request, 'Main_Templates/login.html', {})


def logout_view(request):
    logout(request)
    return redirect("/#about")
