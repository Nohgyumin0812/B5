# Create your models here.
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
from .models import CustomUser


class SignupForm(UserCreationForm):

  def getSports(self, sports):
    self.sports = sports

  class Meta:
    model =CustomUser
    fields = ['username', 'location', 'password1', 'password2', 'email', 'tel', 'sports']
