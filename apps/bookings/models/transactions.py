from django.db import models
from apps.bookings.models.bookings import Bookings

class Transactions(models.Model):
    transaction_id = models.UUIDField(null=False, unique=True)
    booking = models.ForeignKey(Bookings, null=False, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    payment_requested_time = models.DateTimeField(null=True)
    payment_received_time = models.DateTimeField(null=True)
    transaction_reference_id = models.CharField(max_length=200, null=True)
    reversed  = models.BooleanField(default=False)
    dispute  = models.BooleanField(default=False)
    
    class Meta:
        db_table = "transactions"
        verbose_name = "transactions"

