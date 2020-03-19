from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import *

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=inventory_BD.objects.all(), template_name="inventory/index.html")),
    path('users/', ListView.as_view(queryset=Ad_users.objects.all(), template_name="inventory/UserPortal.html")),
]
