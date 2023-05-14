import uuid
from django.db import models
from lens35.constanst import COST_CATEGORIES
from apps.bookings.models.services import Services
from apps.bookings.models.transactions import Transactions

'''
#This is an array to the Service object
    - A service can have multiple service invoice items
    - Like the 
        * actual cost of the service
        * discount
        * cancellation charge
'''
class ServiceInvoiceItems(models.Model):
    
    invoice_item_id = models.UUIDField(null=False, unique=True, default=uuid.uuid4)
    service = models.ForeignKey(Services, null=False, on_delete=models.CASCADE)
    cost_category = models.CharField(max_length=20, null=False, choices= COST_CATEGORIES)
    description = models.CharField(max_length=100, null=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    transaction = models.ForeignKey(Transactions, null=True, on_delete=models.CASCADE)
   
    class Meta:
        db_table = "service_invoice_items"
        verbose_name = "service_invoice_items"