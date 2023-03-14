from django.db import models

class CustomerToken(models.Model):
    mobile_number = models.CharField(max_length=10, null=False)
    customer_id = models.UUIDField(null=False)
    device_id = models.UUIDField(null=False)
    token = models.UUIDField(null=False)
    created_time = models.DateTimeField(null=False, auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=False)
    keep_active = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = "customer_token"
        unique_together = ("mobile_number","device_id", "token")