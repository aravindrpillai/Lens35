from django.db import models

class Customers(models.Model):
    customer_id = models.UUIDField(unique=True)
    full_name = models.CharField(max_length=100, null=True)
    mobile_number = models.CharField(max_length=10, null=False, unique=True)

    email_id = models.EmailField(null=True, unique=True)
    email_id_verified = models.BooleanField(default=False)
    
    subscribe_for_updates = models.BooleanField(default=True)

    display_picture = models.CharField(max_length=50, null=True, unique=True)
    
    class Meta:
        db_table = "customers"
        verbose_name = "customers"