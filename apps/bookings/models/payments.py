from django.db import models

class Payment(models.Model):
    
    payment_id = models.UUIDField(null=False, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    dispute  = models.BooleanField(default=False)
    
    class Meta:
        db_table = "payment"
        verbose_name = "payment"