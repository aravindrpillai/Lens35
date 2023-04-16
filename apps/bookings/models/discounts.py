from django.db import models

class BookingDiscountCodes(models.Model):
    code = models.CharField(max_length=10, null=True)
    expiry = models.DateField(null=False)
    discount_percentage = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    
    class Meta:
        db_table = "booking_discount_codes"
        verbose_name = "booking_discount_codes"