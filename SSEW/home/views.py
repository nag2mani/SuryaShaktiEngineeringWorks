from django.shortcuts import render, redirect
from .models import Expenses
from .forms import ExpensesForm

def expense(request):
    expenses_from_database = Expenses.objects.all()
    total_cash_expenses = sum(expense.cash_expenses for expense in expenses_from_database)
    total_online_expenses = sum(expense.online_expenses for expense in expenses_from_database)
    total_expenses = total_cash_expenses + total_online_expenses
    
    context = {
        'expenses_list_all': expenses_from_database,
        'total_expenses': total_expenses,
    }
    
    return render(request, 'index.html', context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense')  # Redirect to the expense view after saving
    else:
        form = ExpensesForm()
    
    return render(request, 'add_expense.html', {'form': form})
