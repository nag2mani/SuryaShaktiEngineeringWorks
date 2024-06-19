from django import forms
from .models import Expenses

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['online_expenses', 'cash_expenses', 'name_of_person', 'category', 'remark']
        widgets = {
            'online_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'cash_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'name_of_person': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }
