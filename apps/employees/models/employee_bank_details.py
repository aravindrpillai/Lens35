from django.db import models

class EmployeeBankDetails(models.Model):

    bank_details_id = models.UUIDField(unique=True)
    bank = models.CharField(max_length=80, null=False)
    branch = models.CharField(max_length=100, null=False)
    ifsc = models.CharField(max_length=20, null=False)
    account_holder = models.CharField(max_length=60, null=False)
    mobile_number = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "employee_bank_details"
        verbose_name = "employee_bank_details"