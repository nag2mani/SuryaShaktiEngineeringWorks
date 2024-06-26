from django.http import HttpResponse
from .models import *
from .forms import *
from openpyxl import Workbook
from io import BytesIO

def generate_fund_expense_report_xlsx(from_date, to_date):
    # Filter data based on the date range
    expenses = Expenses.objects.filter(date_time__range=[from_date, to_date])
    funds = FundIn.objects.filter(date_time__range=[from_date, to_date])

    # Create a workbook and add a worksheet.
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Fund Expense Report"

    # Define the headers
    expense_headers = ['Date', 'Online Expenses', 'Cash Expenses', 'Name of Person', 'Category', 'Remark']
    fund_headers = ['Date', 'Online Fund', 'Cash Fund', 'Fund Head', 'Category', 'Remark']

    # Write headers for expenses
    for col_num, header in enumerate(expense_headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write expense data
    row = 2
    for expense in expenses:
        worksheet.cell(row=row, column=1, value=str(expense.date_time))
        worksheet.cell(row=row, column=2, value=expense.online_expenses)
        worksheet.cell(row=row, column=3, value=expense.cash_expenses)
        worksheet.cell(row=row, column=4, value=expense.name_of_person)
        worksheet.cell(row=row, column=5, value=expense.category.name)
        worksheet.cell(row=row, column=6, value=expense.remark)
        row += 1

    # Leave a row blank
    row += 1

    # Write headers for fund in
    for col_num, header in enumerate(fund_headers, 1):
        worksheet.cell(row=row, column=col_num, value=header)

    # Write fund in data
    row += 1
    for fund in funds:
        worksheet.cell(row=row, column=1, value=str(fund.date_time))
        worksheet.cell(row=row, column=2, value=fund.online_fund)
        worksheet.cell(row=row, column=3, value=fund.cash_fund)
        worksheet.cell(row=row, column=4, value=fund.name)
        worksheet.cell(row=row, column=5, value=fund.category.name)
        worksheet.cell(row=row, column=6, value=fund.remark)
        row += 1

    # Save the workbook to a BytesIO object
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # Create the HttpResponse
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=fund_expense_report.xlsx'

    return response

def generate_employee_report_xlsx():
    pass

def generate_inventory_report_xlsx():
    pass