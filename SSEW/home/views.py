from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Expenses, FundIn, Employee, Inventory
from django.utils.dateparse import parse_date
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas
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


def generate_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    report_type = request.GET.get('report_type')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if report_type == 'fund_expense':
            format_type = request.GET.get('format_type', 'xlsx')
            if format_type == 'xlsx':
                return generate_fund_expense_report_xlsx(from_date, to_date)
            elif format_type == 'pdf':
                return generate_fund_expense_report_pdf(from_date, to_date)
        elif report_type == 'employee':
            format_type = request.GET.get('format_type', 'xlsx')
            if format_type == 'xlsx':
                return generate_employee_report_xlsx(from_date, to_date)
            elif format_type == 'pdf':
                return generate_employee_report_pdf(from_date, to_date)
        elif report_type == 'inventory':
            format_type = request.GET.get('format_type', 'xlsx')
            if format_type == 'xlsx':
                return generate_inventory_report_xlsx(from_date, to_date)
            elif format_type == 'pdf':
                return generate_inventory_report_pdf(from_date, to_date)
        elif report_type == 'employee_pdf':
            return generate_employee_report_pdf(from_date, to_date)
        elif report_type == 'inventory_pdf':
            return generate_inventory_report_pdf(from_date, to_date)
        # Add similar conditions for other report types and formats
    else:
        return render(request, 'report.html')

    return render(request, 'report.html')  # Handle other cases or errors as needed


def generate_fund_expense_report_xlsx(from_date, to_date):
    expenses = Expenses.objects.filter(date__range=[from_date, to_date])
    fund_ins = FundIn.objects.filter(date__range=[from_date, to_date])

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    headers = ['Date', 'Description', 'Amount', 'Type']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    row_num = 1
    for expense in expenses:
        worksheet.write(row_num, 0, str(expense.date))
        worksheet.write(row_num, 1, expense.description)
        worksheet.write(row_num, 2, expense.amount)
        worksheet.write(row_num, 3, 'Expense')
        row_num += 1

    for fund_in in fund_ins:
        worksheet.write(row_num, 0, str(fund_in.date))
        worksheet.write(row_num, 1, fund_in.description)
        worksheet.write(row_num, 2, fund_in.amount)
        worksheet.write(row_num, 3, 'Fund In')
        row_num += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=fund_expense_report.xlsx'

    return response




def generate_fund_expense_report_pdf(from_date, to_date):
    expenses = Expenses.objects.filter(date__range=[from_date, to_date])
    fund_ins = FundIn.objects.filter(date__range=[from_date, to_date])

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, "Fund and Expense Report")
    
    y = 750
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Description")
    p.drawString(250, y, "Amount")
    p.drawString(350, y, "Type")

    y -= 20
    for expense in expenses:
        p.drawString(50, y, str(expense.date))
        p.drawString(150, y, expense.description)
        p.drawString(250, y, str(expense.amount))
        p.drawString(350, y, 'Expense')
        y -= 20

    for fund_in in fund_ins:
        p.drawString(50, y, str(fund_in.date))
        p.drawString(150, y, fund_in.description)
        p.drawString(250, y, str(fund_in.amount))
        p.drawString(350, y, 'Fund In')
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=fund_expense_report.pdf'

    return response




def generate_inventory_report_xlsx(from_date, to_date):
    inventory_items = Inventory.objects.filter(date_time__range=[from_date, to_date])

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    headers = ['Date', 'Item Name', 'Quantity', 'Price', 'Remark']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, item in enumerate(inventory_items, 1):
        worksheet.write(row_num, 0, str(item.date_time))
        worksheet.write(row_num, 1, item.name)
        worksheet.write(row_num, 2, item.quantity)
        worksheet.write(row_num, 3, item.price)
        worksheet.write(row_num, 4, item.remark)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_report.xlsx'

    return response

def generate_inventory_report_pdf(from_date, to_date):
    inventory_items = Inventory.objects.filter(date_time__range=[from_date, to_date])

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, "Inventory Report")
    
    y = 750
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Item Name")
    p.drawString(250, y, "Quantity")
    p.drawString(350, y, "Price")
    p.drawString(450, y, "Remark")

    y -= 20
    for item in inventory_items:
        p.drawString(50, y, str(item.date_time))
        p.drawString(150, y, item.name)
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, str(item.price))
        p.drawString(450, y, item.remark)
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=inventory_report.pdf'

    return response





def generate_employee_report_xlsx(from_date, to_date):
    employees = Employee.objects.filter(date_time__range=[from_date, to_date])

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    headers = ['Date', 'Name', 'Position', 'Salary', 'Remark']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, employee in enumerate(employees, 1):
        worksheet.write(row_num, 0, str(employee.date_time))
        worksheet.write(row_num, 1, employee.name)
        worksheet.write(row_num, 2, employee.position)
        worksheet.write(row_num, 3, employee.salary)
        worksheet.write(row_num, 4, employee.remark)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employee_report.xlsx'

    return response

def generate_employee_report_pdf(from_date, to_date):
    employees = Employee.objects.filter(date_time__range=[from_date, to_date])

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, "Employee Report")
    
    y = 750
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Name")
    p.drawString(250, y, "Position")
    p.drawString(350, y, "Salary")
    p.drawString(450, y, "Remark")

    y -= 20
    for employee in employees:
        p.drawString(50, y, str(employee.date_time))
        p.drawString(150, y, employee.name)
        p.drawString(250, y, employee.position)
        p.drawString(350, y, str(employee.salary))
        p.drawString(450, y, employee.remark)
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=employee_report.pdf'

    return response

