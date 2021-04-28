from django import forms
from .models import Bug

class BugRegisterForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ('name','description','reproduce')
    
    