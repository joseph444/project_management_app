from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

roles = ['BackEnd Dev','FrontEnd Dev','FullStackDev','HR','PR','Team Lead','DevOps','Database Admin',
        'Network Admin','Management']

class ProfileRegisterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=roles,required=True)
    class Meta:
        model = Profile
        fields = ('pro_picture','role','username','bio')
    

class ProfileChangeForm(forms.Form):
    role = forms.CharField(required=True)
    bio  = forms.CharField(required=False)
    pro_picture = forms.ImageField(required=False)

    

        