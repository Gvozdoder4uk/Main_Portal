from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import *
from Request_Access.models import UserProfile
from django.core.paginator import Paginator

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=inventory_BD.objects.all(), template_name="inventory/index.html")),
    path('users/', ListView.as_view(queryset=UserProfile.objects.all().order_by('user_dep'), template_name="inventory/UserPortal.html")),
    url(r'access/', views.access, name='access_test'),
    path('portal/', views.portal_test, name="portal"),

]
