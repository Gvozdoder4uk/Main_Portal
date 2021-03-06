from django.conf.urls import url, include
from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from .models import *
from django.core.paginator import Paginator

urlpatterns = [
    path('', views.m_access, name='req_index'),
    path('multi/', views.m_access, name='multi'),
    path('cabinet/', views.cabinet,
         name='all_requests'),
    path('personal_cabinet/', views.personal_cabinet, name="my_requests"),
    path('request_actions/', views.request_actions, name="request_actions"),
    path('accepted_requests/', views.accepted_requests, name="accepted_requests"),
    path('detail/<int:id>', views.RequestActionDetail, name="request_detail"),
    path('account/', ListView.as_view(queryset=Access.objects.all(), template_name="request_access/account.html")),
    path('test_cabinet/',
         ListView.as_view(queryset=Access.objects.all(), template_name="request_access/Test_Access.html")),
    path('manager_page/', views.manager_page , name="manager"),
    # path('test_requests/', views.requests),
    #path('created_task/<int:id>', views.created_task, name="created_task"),
    path('test_requests/', views.RequestListView.as_view(), name="request"),
    # path('test_requests/detail/<int:id>', views.request_detail, name="detail")
    # path('test_requests/detail/<int:pk>', views.RequestDetailView.as_view(), name="detail"),
    # path('test_requests/detail/edit_page', views.edit_request, name="edit_request"),
    url('email/', views.email, name='email'),
]
