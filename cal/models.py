from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import CustomUser

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

"""
class group(models.Model):
    user_group = models.OneToOneField('user_group')
"""

class CustomGroup(models.Model):
    groupname = models.CharField('groupname', max_length=200, blank=False, null=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner', null = True, blank = True)
    members = models.ManyToManyField(CustomUser, verbose_name='members', related_name='members', blank = True, default='')
    #date = models.DateTimeField(null = True, blank = True, default='')
    sports = models.CharField(max_length=50, default='')
    friendname = models.CharField(max_length=50, default='')