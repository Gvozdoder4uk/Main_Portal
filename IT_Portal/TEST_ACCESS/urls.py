from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import *
from django.core.paginator import Paginator

urlpatterns = [
    url(r'^$', views.index, name='main')
]