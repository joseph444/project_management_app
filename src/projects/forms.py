from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name','description','budget')


class ProjectEditForm(forms.Form):
    project_name = forms.CharField(max_length=200,required=True)
    description = forms.CharField(required=True)
    budget = forms.FloatField(required=True)
    isClosed = forms.BooleanField(required=False)