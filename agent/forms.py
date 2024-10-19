from .models import Agent
from django import forms



class UpdateAgentForm(forms.ModelForm):
    class Meta:
        model = Agent

        fields=('full_name','address','country','mobile_no','photo','division','district','thana','birth_date')
