from django.contrib import admin
from cal.models import Event
# Register your models here.
from common.models import CustomUser

admin.site.register(CustomUser)