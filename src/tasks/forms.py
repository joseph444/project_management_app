from django import forms
from .models import Task


class TaskCreationForm(forms.Form):
    assigned_to = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    resources = forms.CharField(required=False)
    deadline = forms.DateTimeField(required=False)

    