from django.forms import ModelForm
from cal.models import Event

class SignupForm(ModelForm):
  password_check = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'pw2'}))
  class Meta:
      model = Member
      fields = ['username', 'password', 'password_check', 'name']
      widgets = {
        'username' : forms.TextInput(attrs={'class':'username'}),
        'password' : forms.PasswordInput(attrs={'class':'pw1'})
      }
