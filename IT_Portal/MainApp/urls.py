from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth import logout

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'night/', views.daynight, name='daynight')
]

urlpatterns += [
    path('signin/', views.loginpage, name='loginpage'),
    path('logout/', views.logout_view, name='logout'),
]
