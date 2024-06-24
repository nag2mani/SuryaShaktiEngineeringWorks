from django.http import HttpResponse
from .models import *
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas


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
    pass

def generate_employee_report_xlsx(from_date, to_date):
    pass