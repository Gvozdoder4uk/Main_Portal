from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='relax'),
    path('panels/', views.panels, name='infopanels')
]
