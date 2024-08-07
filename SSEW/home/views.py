from .forms import *
from .models import *
from .report import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect

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


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).all()
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


def load_subsources(request):
    source_id = request.GET.get('source')
    subsources = SubSource.objects.filter(source_id=source_id).all()
    return JsonResponse(list(subsources.values('id', 'name')), safe=False)


def add_expense(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            # To send message on Template.
            messages.success(request, 'Expense added successfully!')
            return redirect('add_expense')
    else:
        form = ExpensesForm()
    return render(request, 'add_expense.html', {'form': form})


def add_fund(request):
    if request.method == 'POST':
        form = FundInForm(request.POST)
        if form.is_valid():
            form.save()
            # To send message on Template.
            messages.success(request, 'Fund added successfully!')
            return redirect('add_fundin')
    else:
        form = FundInForm()
    return render(request, 'add_fundin.html', {'form': form})


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})


def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InventoryForm()
    return render(request, 'add_inventory.html', {'form': form})


def all_data(request):
    expenses = Expenses.objects.all()
    fundin = FundIn.objects.all()
    employees = Employee.objects.all()
    inventory = Inventory.objects.all()

    context = {
        'expenses': expenses,
        'fundin': fundin,
        'employees': employees,
        'inventory': inventory,
    }
    return render(request, 'all_data.html', context)


def generate_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    report_type = request.GET.get('report_type')
    category_id = request.GET.get('expense_category')
    source_id = request.GET.get('fund_source')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if report_type == 'fund_expense_xlsx':
            return generate_fund_expense_report_xlsx(from_date, to_date)
        elif report_type == 'employee_xlsx':
            return generate_employee_report_xlsx(from_date, to_date)
        elif report_type == 'inventory_xlsx':
            return generate_inventory_report_xlsx(from_date, to_date)
        elif report_type == 'expense_category_wise_report_xlsx':
            return generate_category_wise_report_xlsx(from_date, to_date, category_id)
        elif report_type == 'fundin_source_wise_report_xlsx':
            return generate_source_wise_report_xlsx(from_date, to_date, source_id)
    else:
        return render(request, 'report.html', {'categories': Category.objects.all(), 'sources': Source.objects.all()})