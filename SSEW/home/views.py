from django.shortcuts import render, redirect
from .models import *
from .forms import *

#Instruction : Use and pass only singular variable name throught the application.

def home(request):
    total_cash_expense = Expenses.objects.aggregate(models.Sum('cash_expenses'))['cash_expenses__sum'] or 0
    total_online_expense = Expenses.objects.aggregate(models.Sum('online_expenses'))['online_expenses__sum'] or 0
    total_cash_fund = FundIn.objects.aggregate(models.Sum('cash_fund'))['cash_fund__sum'] or 0
    total_online_fund = FundIn.objects.aggregate(models.Sum('online_fund'))['online_fund__sum'] or 0
    total_fund = total_cash_fund + total_online_fund

    total_expense = total_cash_expense + total_online_expense

    total_cash_in_hand = total_cash_fund - total_cash_expense

    context = {
        'total_expense': total_expense,
        'total_cash_in_hand':total_cash_in_hand
    }
    return render(request, 'index.html', context)


def add_expense(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home
    else:
        form = ExpensesForm()
    
    return render(request, 'add_expense.html', {'form': form})



def add_fund(request):
    if request.method == 'POST':
        form = FundInForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home
    else:
        form = FundInForm()
    return render(request, 'add_fundin.html', {'form': form})


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})


