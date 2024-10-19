from django import forms
#from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User 
from .models import Profile
#from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)
        

class InfoProfileForm(forms.ModelForm):

    class Meta():
        model=Profile
        fields = ('full_name','address','country','mobile_no',)