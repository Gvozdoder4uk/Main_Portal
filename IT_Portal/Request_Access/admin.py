from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Access)
admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(Requests)
admin.site.register(Mails)
admin.site.register(InformationSecurity)
admin.site.register(ApproveList)

admin.site.register(Address)
admin.site.register(Store)