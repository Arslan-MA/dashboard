from django.contrib import admin
from app.models import *

admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Bottle)
admin.site.register(Order)
admin.site.register(Revenue)
admin.site.register(DailyRevenue)
admin.site.register(WeeklyRevenue)
admin.site.register(MonthlyRevenue)
