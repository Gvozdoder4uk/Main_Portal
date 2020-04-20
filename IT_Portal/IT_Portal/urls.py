"""IT_Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url('^', include('MainApp.urls'), name='start_page'),
                  path('admin/', admin.site.urls, name='admin_page'),
                  path('inventory/', include('inventory.urls'), name='inventory'),
                  path('relax_portal/', include('relax_portal.urls'), name='relax_portal'),
                  path('requests/', include('Request_Access.urls'), name='requests')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
