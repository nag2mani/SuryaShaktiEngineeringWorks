from django.contrib import admin
from .models import *

# Model Registration.
admin.site.register(Expenses)
admin.site.register(FundIn)
admin.site.register(Employee)
admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Source)
admin.site.register(SubSource)