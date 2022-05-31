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
    friendname = models.CharField(max_length=50, default='')

class DayGroup(models.Model):
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='group', null = True, blank = True)
    dates = models.CharField(max_length=100, default='')


"""
    # title 새로 저장 시, slug 에 해당 title slugify하여 저장
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.groupname, allow_unicode=True)
        super(CustomGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupname

class InviteStatus(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete = models.CASCADE, related_name = 'invites')
    invited = models.ManyToManyField(CustomUser, related_name = 'invited', blank = True)
    accepted = models.ManyToManyField(CustomUser, related_name='accepted', blank=True)
    rejected = models.ManyToManyField(CustomUser, related_name='rejected', blank=True)

    def __str__(self):
        return self.group.groupname

"""