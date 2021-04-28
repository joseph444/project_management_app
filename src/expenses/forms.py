from django import forms
from .models import Expense

class ExpenseCreationForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name','description','expense')