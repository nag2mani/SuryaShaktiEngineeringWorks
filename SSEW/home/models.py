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
    name_of_person = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    remark = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name_of_person} - {self.online_expenses} - {self.cash_expenses} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"

