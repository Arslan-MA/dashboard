from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.phone_number}"


class Employee(models.Model):
    name = models.CharField(max_length=255)

    CHOICE_STATUS = [
        ('free', 'Free'),
        ('busy', 'Busy'),
    ]

    status = models.CharField(max_length=255, choices=CHOICE_STATUS)

    def __str__(self):
        return f"{self.name} - {self.status}"


class Bottle(models.Model):
    CHOICE_TYPE = [
        ('2 liters', '2 liters'),
        ('5 liters', '5 liters'),
        ('10 liters', '10 liters'),
    ]

    bottle_type = models.CharField(max_length=255, choices=CHOICE_TYPE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bottle_type} - {self.quantity}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    CHOICE_TYPE = [
        ('2 liters', '2 liters'),
        ('5 liters', '5 liters'),
        ('10 liters', '10 liters'),
    ]

    bottle_type = models.CharField(max_length=255, choices=CHOICE_TYPE)
    quantity = models.PositiveIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    CHOICE_STATUS = [
        ('in progress', 'In progress'),
        ('delivered', 'Delivered'),
    ]

    status = models.CharField(max_length=255, choices=CHOICE_STATUS)

    def __str__(self):
        return f"{self.client.name} - {self.quantity} - {self.employee.name} - {self.status}"


class Revenue(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_total_revenue()

    @staticmethod
    def update_total_revenue():
        today_revenue = Revenue.objects.filter(
            created_at__date=now().date()).aggregate(total=Sum('amount')).get('total')
        week_revenue = Revenue.objects.filter(
            created_at__week=now().isocalendar()[1]).aggregate(total=Sum('amount')).get('total')
        month_revenue = Revenue.objects.filter(
            created_at__month=now().month).aggregate(total=Sum('amount')).get('total')

        DailyRevenue.objects.update_or_create(date=now().date(), defaults={'total_revenue': today_revenue})
        WeeklyRevenue.objects.update_or_create(week=now().isocalendar()[1], defaults={'total_revenue': week_revenue})
        MonthlyRevenue.objects.update_or_create(month=now().month, defaults={'total_revenue': month_revenue})


class DailyRevenue(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Выручка за {self.date}"


class WeeklyRevenue(models.Model):
    week = models.PositiveSmallIntegerField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Выручка за неделю {self.week}"


class MonthlyRevenue(models.Model):
    month = models.PositiveSmallIntegerField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Выручка за месяц {self.month}"
