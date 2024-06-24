from django import forms
from .models import *

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['online_expenses', 'cash_expenses', 'name_of_person', 'remark', 'is_employee_expense', 'employee', 'category', 'subcategory']
        widgets = {
            'online_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'cash_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'name_of_person': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
            'is_employee_expense': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
        }


class FundInForm(forms.ModelForm):
    class Meta:
        model = FundIn
        fields = ['online_fund', 'cash_fund', 'fund_head', 'category', 'subcategory', 'remark']
        widgets = {
            'online_fund': forms.NumberInput(attrs={'class': 'form-control'}),
            'cash_fund': forms.NumberInput(attrs={'class': 'form-control'}),
            'fund_head': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'mobile1', 'mobile2', 'aadhar_number', 'salary', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile1': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile2': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'account': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['inventory_name', 'quantity', 'total_price', 'remark']
        widgets = {
            'inventory_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }



        