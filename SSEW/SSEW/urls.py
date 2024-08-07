"""
URL configuration for SSEW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', home, name='home'),
    path('add_expense/', add_expense, name='add_expense'),
    path('add_fundin/', add_fund, name='add_fundin'),
    path('add_employee/', add_employee, name='add_employee'),
    path('add_inventory/', add_inventory, name='add_inventory'),
    path('report/', generate_report, name='generate_report'),
    path('ajax/load-subcategories/', load_subcategories, name='load_subcategories'),
    path('ajax/load-subsources/', load_subsources, name='load_subsources'),
    path('fund_expense_list/', fund_expense_list, name='fund_expense_list'),
    path('employee_list/', employee_list, name='employee_list'),
    path('inventory_list/', inventory_list, name='inventory_list'),
    path('all_data/', all_data, name='all_data'),
    path('admin/', admin.site.urls)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


