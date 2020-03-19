from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(inventory_BD)


@admin.register(Ad_users)
class Users_Admin(admin.ModelAdmin):
    list_display = ('user_lastname','user_firstname', 'user_secondname','user_dep','user_otdel','user_desc')

    fieldsets = (
        ("Основные данные", {
            'fields': ('user_firstname', 'user_lastname', 'user_secondname', 'user_birth')
        }),
        ('Рабочие данные', {
            'fields': ('user_dep', 'user_otdel')
        }),
        ('Допольнительная информация ', {
            'fields': ('user_photo', 'user_desc')
        })
    )
