from django.db import models
from apps.bookings.models.services import Services
from apps.employees.models.employees import Employees

class EmployeePreference(models.Model):
    service = models.ForeignKey(Services, null=False, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "employee_preference"
        verbose_name = "employee_preference"