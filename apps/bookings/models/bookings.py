from django.db import models
from apps.customers.models import Customers
from lens35.constanst import EVENTS

class Bookings(models.Model):

    booking_id = models.UUIDField(null=False, unique=True)
    created_time = models.DateTimeField(null=False, auto_now_add=True)
    
    event = models.CharField(max_length=20, null=False, choices= EVENTS)
    event_description = models.CharField(max_length=500, null=True)
    
    event_date = models.DateField(null=False)
    event_start_time = models.TimeField(null=False)
    event_duration = models.IntegerField(null=False)
    
    event_postal_code = models.CharField(max_length=7, null=False)
    event_city = models.CharField(max_length=50, null=False)
    event_address = models.CharField(max_length=150, null=False)
    event_latitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)
    event_longitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)

    lifecycle = models.JSONField(null=True)
    customer = models.ForeignKey(Customers, null=False, on_delete=models.CASCADE)

    #this flag will be turned to true, once the customer finalises the booking and the payment is done
    #bookings will be avilable to employees only when the published flag is true 
    published = models.BooleanField(default=False)
    
    class Meta:
        db_table = "bookings"
        verbose_name = "bookings"

    