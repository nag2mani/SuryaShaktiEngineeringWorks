from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from .report import *
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

def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).all()
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

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

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if report_type == 'fund_expense_xlsx':
            return generate_fund_expense_report_xlsx(from_date, to_date)
        elif report_type == 'employee_xlsx':
            return generate_employee_report_xlsx(from_date, to_date)
        elif report_type == 'inventory_xlsx':
            return generate_inventory_report_xlsx(from_date, to_date)
        elif report_type == 'category_wise_report_xlsx':
            return generate_category_wise_report_xlsx(from_date, to_date)
    else:
        return render(request, 'report.html')


def fund_expense_list(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    id = request.GET.get('id')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if id == 'fund_expense_list':
            expenses = Expenses.objects.filter(date_time__range=[from_date, to_date])
            funds = FundIn.objects.filter(date_time__range=[from_date, to_date])
            fund_expense_list = list(expenses) + list(funds)  # Combine querysets into a list
            return render(request, 'fund_expense_list.html', {'fund_expense_list': fund_expense_list})
    
    return render(request, 'fund_expense_list.html', {'fund_expense_list': []})


def employee_list(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    id = request.GET.get('id')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if id == 'employee_list':
            employees = Employee.objects.filter(date_time__range=[from_date, to_date])
            return render(request, 'employee_list.html', {'employees': employees})

    return render(request, 'employee_list.html', {'employees': []})


def inventory_list(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    id = request.GET.get('id')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if id == 'inventory_list':
            inventories = Inventory.objects.filter(date_time__range=[from_date, to_date])
            return render(request, 'inventory_list.html', {'inventories': inventories})

    return render(request, 'inventory_list.html', {'inventories': []})

