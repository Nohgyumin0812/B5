from django.forms import ModelForm, DateInput
from cal.models import Event
from .models import *
from django import forms


class EventForm(ModelForm):
  class Meta:
    model = Event
    widgets = {
      'date': DateInput(attrs={'type': 'datetime'}, format='%Y-%m-%d'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['date'].input_formats = ('%Y-%m-%d',)



class GroupForm(forms.ModelForm):

  class Meta:
    model = CustomGroup
    fields = ["groupname", "sports", "friendname", "location", "location_code", "x", "y", "dateFirst", "sportFirst"]


class DayForm(forms.ModelForm):

  class Meta:
    model = DayGroup
    fields = ["group", "myDates", "user"]


class InviteForm(forms.ModelForm):

  class Meta:
    model = InviteGroup
    fields = ["invite_user", "group", "invite_status"]

class ScheForm(forms.ModelForm):

  class Meta:
    model = ScheGroup
    fields = ['sche_name', 'sche_date', 'sche_memo', 'group_id']
