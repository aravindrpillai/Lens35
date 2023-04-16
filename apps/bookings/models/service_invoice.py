from django.db import models
from apps.bookings.models.services import Services

class ServiceInvoice(models.Model):
    
    service = models.OneToOneField(Services, null=False, on_delete=models.CASCADE)
    service_amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    discount_code = models.CharField(max_length=10, null=True)
    other_cost = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    final_amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    transaction_id = models.UUIDField(null=True) #If transaction id of the payment - avoid FK relation
    paid  = models.BooleanField(default=False)

    class Meta:
        db_table = "service_invoice"
        verbose_name = "service_invoice"