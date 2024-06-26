from django.http import HttpResponse
from .models import *
from .forms import *
from openpyxl import Workbook
from io import BytesIO
import pytz

def generate_fund_expense_report_xlsx(from_date, to_date):
    # Filter data based on the date range
    expenses = Expenses.objects.filter(date_time__range=[from_date, to_date])
    funds = FundIn.objects.filter(date_time__range=[from_date, to_date])

    # Create a workbook and add a worksheet.
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Fund Expense Report"

    # Define the headers based on model fields
    expense_headers = [field.name for field in Expenses._meta.fields]
    fund_headers = [field.name for field in FundIn._meta.fields]

    # Write headers for expenses
    for col_num, header in enumerate(expense_headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write expense data
    row = 2
    for expense in expenses:
        for col_num, field in enumerate(expense_headers, 1):
            value = getattr(expense, field)
            if isinstance(value, (pytz.datetime.datetime, pytz.datetime.time)):
                value = value.replace(tzinfo=None)
            if field in ['category', 'subcategory', 'employee'] and value:
                value = str(value)
            worksheet.cell(row=row, column=col_num, value=value)
        row += 1

    # Leave a row blank
    row += 1

    # Write headers for fund in
    for col_num, header in enumerate(fund_headers, 1):
        worksheet.cell(row=row, column=col_num, value=header)

    # Write fund in data
    row += 1
    for fund in funds:
        for col_num, field in enumerate(fund_headers, 1):
            value = getattr(fund, field)
            if isinstance(value, (pytz.datetime.datetime, pytz.datetime.time)):
                value = value.replace(tzinfo=None)
            if field in ['category', 'subcategory', 'received_by'] and value:
                value = str(value)
            worksheet.cell(row=row, column=col_num, value=value)
        row += 1

    # Save the workbook to a BytesIO object
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # Create the HttpResponse
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=fund_expense_report.xlsx'

    return response




def generate_employee_report_xlsx(from_date, to_date):
    # Filter data based on the date range
    employees = Employee.objects.filter(date_time__range=[from_date, to_date])

    # Create a workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Employee Report"

    # Define the headers based on model fields
    headers = [field.name for field in Employee._meta.fields]

    # Write headers
    for col_num, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write employee data
    row = 2
    for employee in employees:
        for col_num, field in enumerate(headers, 1):
            value = getattr(employee, field)
            if isinstance(value, (pytz.datetime.datetime, pytz.datetime.time)):
                value = value.replace(tzinfo=None)
            worksheet.cell(row=row, column=col_num, value=value)
        row += 1

    # Save the workbook to a BytesIO object
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # Create the HttpResponse
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employee_report.xlsx'

    return response




def generate_inventory_report_xlsx(from_date, to_date):
    # Filter data based on the date range
    inventories = Inventory.objects.filter(date_time__range=[from_date, to_date])

    # Create a workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Inventory Report"

    # Define the headers based on model fields
    headers = [field.name for field in Inventory._meta.fields]

    # Write headers
    for col_num, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write inventory data
    row = 2
    for inventory in inventories:
        for col_num, field in enumerate(headers, 1):
            value = getattr(inventory, field)
            if isinstance(value, (pytz.datetime.datetime, pytz.datetime.time)):
                value = value.replace(tzinfo=None)
            worksheet.cell(row=row, column=col_num, value=value)
        row += 1

    # Save the workbook to a BytesIO object
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # Create the HttpResponse
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_report.xlsx'

    return response