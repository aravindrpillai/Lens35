from django.db import models
from apps.bookings.models.payments import Payment

class Transactions(models.Model):
    transaction_id = models.UUIDField(null=False, unique=True)
    payment = models.ForeignKey(Payment, null=False, on_delete=models.CASCADE)
    payment_requested_time = models.DateTimeField(null=True)
    payment_received_time = models.DateTimeField(null=True)
    transaction_reference_id = models.CharField(max_length=200, null=True)
    reversed  = models.BooleanField(default=False)
    dispute  = models.BooleanField(default=False)
    
    class Meta:
        db_table = "transactions"
        verbose_name = "transactions"

