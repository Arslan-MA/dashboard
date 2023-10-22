from django.shortcuts import render
from django.views.generic import ListView
from app.models import *


class OrderListView(ListView):
    template_name = 'app/orders_page.html'
    model = Order
    context_object_name = 'orders'


class ProductListView(ListView):
    template_name = 'app/products_page.html'
    model = Bottle
    context_object_name = 'products'


class ClientsPageView(ListView):
    template_name = 'app/clients_page.html'
    model = Client
    context_object_name = 'clients'


class EmployeesPageView(ListView):
    template_name = 'app/employees_page.html'
    model = Employee
    context_object_name = 'employees'


def revenue_page(request):
    context = {'daily_revenue': DailyRevenue.objects.all(),
               'weekly_revenue': WeeklyRevenue.objects.all(),
               'monthly_revenue': MonthlyRevenue.objects.all()}

    return render(request, 'app/revenue_page.html', context)
