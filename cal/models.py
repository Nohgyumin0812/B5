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
    groupname = models.CharField('groupname', max_length=200, blank=False, null=False, unique = True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner', null = True, blank = True)
    members = models.ManyToManyField(CustomUser, verbose_name='members', related_name='members', blank = True, default='')
    sports = models.CharField(max_length=50, default='')
    friendname = models.CharField(max_length=50, default='', blank = True)
    location =models.CharField(max_length=50, default='', blank = True)
    location_code = models.CharField(max_length=50, default='', blank = True)
    x = models.CharField(max_length=50, default='', blank = True)
    y = models.CharField(max_length=50, default='', blank = True)
    dateFirst = models.CharField(max_length=50, default='', blank = True)
    sportFirst = models.CharField(max_length=50, default='', blank = True)

class DayGroup(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, verbose_name='group', null = True, blank = True)
    myDates = models.CharField(max_length=100, default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner', null = True, blank = True)



class InviteGroup(models.Model):
    invite_user = models.CharField(max_length=50, default='', blank = True)
    group = models.CharField(max_length=50, default='', blank = True)
    invite_status = models.CharField(max_length=50, default='', blank = True)

class viewSeat(models.Model):
    seat = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='viewseat', null = True, blank = True)
    yearmonth = models.DateTimeField()
    day = models.DateTimeField()

class checkSeat(models.Model):
    seat = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='checkseat', null = True, blank = True)
    yearmonth = models.DateTimeField()
    day = models.DateTimeField()

class cancelSeat(models.Model):
    seat = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='cancelseat', null = True, blank = True)
    yearmonth = models.DateTimeField()
    day = models.DateTimeField()

class saveData(models.Model):
    seat = models.CharField(max_length=50, default='', blank = True)
    yearmonth = models.DateTimeField()
    day = models.DateTimeField()



