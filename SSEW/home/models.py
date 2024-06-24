from django.db import models
from django.contrib.auth.models import User

# Models
class Expenses(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    online_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    cash_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    name_of_person = models.CharField(max_length=50, null=True, blank=True)
    remark = models.TextField(blank=True, null=True)
    is_employee_expense = models.BooleanField(default=False)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Expense Name {self.name_of_person or 'Unknown'} on {self.date_time}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Category: {self.category.name})"


class FundIn(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    online_fund = models.DecimalField(max_digits=10, decimal_places=2)
    cash_fund = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    remark = models.TextField(blank=True, null=True)
    received_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"FundIn: {self.name} on {self.date_time}"


class Employee(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    mobile1 = models.CharField(max_length=10)
    mobile2 = models.CharField(max_length=10, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()

    def __str__(self):
        return f"{self.name}, Mobile 1: {self.mobile1}, Aadhar Number: {self.aadhar_number}"


class Inventory(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    inventory_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inventory: {self.inventory_name}, Quantity: {self.quantity}, Total Price: {self.total_price}"