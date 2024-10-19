from django.forms import fields
from .models import Notification,UserExtended
from django import forms
from organization.models import Contact
from user_profile.models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification

        fields=('title','body','member_type','duration')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Notification

        fields=('title','body','member_type','duration')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name','address','country','mobile_no')

class EditAdminForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

class AdminPhotoForm(forms.ModelForm):
    class Meta:
        model =  UserExtended

        fields = ('photo',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields=('name','email','phone','address','message')