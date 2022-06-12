from django.forms import ModelForm, DateInput
from .models import *
from django import forms

class GroupForm(forms.ModelForm):

  class Meta:
    model = CustomGroup
    fields = ["groupname", "sports", "friendname", "location", "location_code", "x", "y", "dateFirst", "sportFirst", "invite_status", "mix_status"]


class DayForm(forms.ModelForm):

  class Meta:
    model = DayGroup
    fields = ["group", "myDates", "user"]


class InviteForm(forms.ModelForm):

  class Meta:
    model = InviteGroup
    fields = ["invite_user", "group", "invite_status"]


class InviteGroupForm(forms.ModelForm):

  class Meta:
    model = InviteGroupGroup
    fields = ["invite_group", "group", "invite_status", "owner_id"]

class ScheForm(forms.ModelForm):

  class Meta:
    model = ScheGroup
    fields = ['sche_name', 'sche_date', 'sche_memo', 'group_id']


class my_ScheForm(forms.ModelForm):

  class Meta:
    model = my_ScheGroup
    fields = ['sche_name', 'sche_date', 'sche_memo', 'user_id']

class mixCustomForm(forms.ModelForm):
  class Meta:
    model = mixCustomGroup
    fields = ["groupname", "sports", "friendname", "location", "location_code", "x", "y", "dateFirst", "sportFirst", "invite_status", "mix_status"]
