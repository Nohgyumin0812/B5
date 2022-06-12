from django.contrib import admin
# Register your models here.
from common.models import CustomUser

admin.site.register(CustomUser)