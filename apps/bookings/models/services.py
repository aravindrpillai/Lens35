from apps.bookings.models.bookings import Bookings
from apps.employees.models import Employees
from lens35.constanst import SERVICES
from django.db import models

class Services(models.Model):

    service_id = models.UUIDField(null=False, unique=True)
    booking = models.ForeignKey(Bookings, null=False, on_delete=models.CASCADE)
    
    created_time = models.DateTimeField(null=False, auto_now_add=True)
    service = models.CharField(max_length=20, null=False, choices= SERVICES)
    
    employee = models.ForeignKey(Employees, null=True, on_delete=models.CASCADE)
    lifecycle = models.JSONField(null=True)
    retired = models.BooleanField(default=False)

    class Meta:
        db_table = "services"
        verbose_name = "services"