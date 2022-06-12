from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import CustomUser
from django.utils.text import slugify


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class CustomGroup(models.Model):
    groupname = models.CharField(max_length=50, default='', blank = True, unique = True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner', null = True, blank = True)
    members = models.ManyToManyField(CustomUser, verbose_name='members', related_name='members', blank = True, default='')
    sports = models.CharField(max_length=50,blank = True, default='')
    friendname = models.CharField(max_length=50, default='', blank = True)
    location =models.CharField(max_length=50, default='', blank = True)
    location_code = models.CharField(max_length=50, default='', blank = True)
    x = models.CharField(max_length=50, default='', blank = True)
    y = models.CharField(max_length=50, default='', blank = True)
    dateFirst = models.CharField(max_length=50, default='', blank = True)
    sportFirst = models.CharField(max_length=50, default='', blank = True)
    invite_status = models.CharField(max_length=50, default='', blank = True)
    mix_status = models.CharField(max_length=50, default='', blank = True)

class DayGroup(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, verbose_name='group', null = True, blank = True)
    myDates = models.CharField(max_length=100, default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner', null = True, blank = True)


class InviteGroup(models.Model):
    invite_user = models.CharField(max_length=50, default='', blank = True)
    group = models.CharField(max_length=50, default='', blank = True)
    invite_status = models.CharField(max_length=50, default='', blank = True)

class InviteGroupGroup(models.Model):
    invite_group = models.CharField(max_length=50, default='', blank = True)
    group = models.CharField(max_length=50, default='', blank = True)
    invite_status = models.CharField(max_length=50, default='', blank = True)
    owner_id = models.CharField(max_length=50, default='', blank = True)

class ScheGroup(models.Model):
    sche_name = models.CharField(max_length=50, default='', blank = True)
    sche_date = models.CharField(max_length=50, default='', blank = True)
    sche_memo = models.CharField(max_length=50, default='', blank = True)
    group_id =  models.CharField(max_length=50, default='', blank = True)

class my_ScheGroup(models.Model):
    sche_name = models.CharField(max_length=50, default='', blank = True)
    sche_date = models.CharField(max_length=50, default='', blank = True)
    sche_memo = models.CharField(max_length=50, default='', blank = True)
    user_id =  models.CharField(max_length=50, default='', blank = True)

class mixCustomGroup(models.Model):
    groupname = models.CharField(max_length=50, default='', blank = True)
    owner = models.CharField(max_length=50, default='', blank = True)
    owner_id = models.CharField(max_length=50,default='',blank=True)
    sports = models.CharField(max_length=50, default='', blank = True)
    friendname = models.CharField(max_length=50, default='', blank = True)
    location =models.CharField(max_length=50, default='', blank = True)
    location_code = models.CharField(max_length=50, default='', blank = True)
    x = models.CharField(max_length=50, default='', blank = True)
    y = models.CharField(max_length=50, default='', blank = True)
    dateFirst = models.CharField(max_length=50, default='', blank = True)
    sportFirst = models.CharField(max_length=50, default='', blank = True)
    invite_status = models.CharField(max_length=50, default='', blank = True)
    mix_status = models.CharField(max_length=50, default='', blank = True)
