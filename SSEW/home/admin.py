from django.contrib import admin
from .models import Employee, Expenses, FundIn, Inventory
# Register your models here.
admin.site.register(Expenses)
admin.site.register(FundIn)
admin.site.register(Employee)
admin.site.register(Inventory)


