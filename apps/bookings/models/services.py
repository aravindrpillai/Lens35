from apps.bookings.models.bookings import Bookings
from apps.employees.models import Employees
from lens35.constanst import SERVICES
from django.db import models

class Services(models.Model):

    service_id = models.UUIDField(null=False, unique=True)
    booking = models.ForeignKey(Bookings, null=False, on_delete=models.CASCADE)
    
    created_time = models.DateTimeField(null=False, auto_now_add=True)
    service = models.CharField(max_length=20, null=False, choices= SERVICES)
    
    employee = models.ForeignKey(Employees, null=True, related_name='employee', on_delete=models.CASCADE)
    lifecycle = models.JSONField(null=True)

    #this will be set to true when the photographer uploads the photos and mark the service as closed.
    closed = models.BooleanField(default=False)
    closed_time = models.DateTimeField(null=True)
    
    #this will be set to true, when the customer deletes the service from the booking
    retired = models.BooleanField(default=False)
    retired_time = models.DateTimeField(null=True)
                                  
    #this will be set to true when there is a update in booking
    # true means the employee associated to this booking needs to review the change and approve or unapprove. 
    # when this is true, the same booking will be published to other employees for a backup.
    # if the current employee approves it, then the backup_employee will be removed.
    # else the current employee will be replayed with the backup employee.                                   
    review = models.BooleanField(default=False)
    employee_backup = models.ForeignKey(Employees, null=True, related_name='employee_backup', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "services"
        verbose_name = "services"