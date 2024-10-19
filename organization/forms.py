

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    # full_name = forms.CharField(required=True)
    # phone = forms.CharField(required=True)
    # email_from = forms.EmailField(required=True)
    # address = forms.TextField(required=True)
    # message = forms.CharField(widget=forms.Textarea, required=True)
    class Meta():
        model=Contact
        fields = ('name','email','address','phone','message',)