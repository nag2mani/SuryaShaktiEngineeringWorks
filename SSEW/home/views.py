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

    # Fetch total number of employees
    total_employees = Employee.objects.count()

    # Fetch recent cash transactions (expenses and fund-ins)
    recent_cash_expense = Expenses.objects.filter(cash_expenses__gt=0).order_by('-date_time')[:2]
    recent_cash_fund_ins = FundIn.objects.filter(cash_fund__gt=0).order_by('-date_time')[:3]

    # Fetch recent online transactions (expenses and fund-ins)
    recent_online_expense = Expenses.objects.filter(online_expenses__gt=0).order_by('-date_time')[:2]
    recent_online_fund_ins = FundIn.objects.filter(online_fund__gt=0).order_by('-date_time')[:3]

    context = {
        'total_expense': total_expense,
        'total_cash_in_hand': total_cash_in_hand,
        'total_employees': total_employees,
        'recent_cash_expense': recent_cash_expense,
        'recent_cash_fund_ins': recent_cash_fund_ins,
        'recent_online_expense': recent_online_expense,
        'recent_online_fund_ins': recent_online_fund_ins,
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


def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home
    else:
        form = InventoryForm()
    return render(request, 'add_inventory.html', {'form': form})