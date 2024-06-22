from django.db import models
from django.contrib.auth.models import User

# These are my models, created for database.

class Expenses(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'SALARY'),
        ('adv_salary', 'ADVANCE SALARY'),
        ('food', 'FOOD'),
        ('petrol', 'PETROL'),
        ('return_money', 'RETURN MONEY'),
        ('rubble', 'RUBBLE'),
        ('stamping_fee', 'STAMPING FEE'),
        ('other', 'OTHERS')
    ]

    date_time = models.DateTimeField(auto_now_add=True)
    online_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    cash_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    name_of_person = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    remark = models.TextField(blank=True, null=True)
    is_employee_expense = models.BooleanField(default=False)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.name_of_person} - {self.online_expenses} - {self.cash_expenses} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"


class FundIn(models.Model):
    CATEGORY_CHOICES = [
        ('return_money', 'RETURN MONEY'),
        ('rubble', 'RUBBLE'),
        ('stamping_fee', 'STAMPING FEE'),
        ('battery', 'BATTERY SERVICE'),
        ('kanta', 'KANTA'),
        ('repairing', 'Repairing'),
        ('other', 'OTHERS')
    ]

    date_time = models.DateTimeField(auto_now_add=True)
    online_fund = models.DecimalField(max_digits=10, decimal_places=2)
    cash_fund = models.DecimalField(max_digits=10, decimal_places=2)
    fund_head = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    remark = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return f"{self.fund_head} - {self.online_fund} - {self.cash_fund} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"


class Employee(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    mobile1 = models.CharField(max_length=10)
    mobile2 = models.CharField(max_length=10, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    # account = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()

    def __str__(self):
        return self.name + ", Mobile 1 : " + self.mobile1 + ", Aadhar Number : " + self.aadhar_number


class Inventory(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    inventory_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return self.inventory_name

