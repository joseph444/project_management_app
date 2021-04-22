from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.exceptions import ValidationError
from .models import Users

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Users
        fields = ('email','first_name','last_name','password1','password2')
    
    def save(self, commit=True):
            user = super(RegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
            
    def clean_email(self):
        email = self.cleaned_data['email']
        if Users.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
    



class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Users.objects.filter(email=email).exists():
            raise ValidationError("Email or Password is incorrect")
        return email


