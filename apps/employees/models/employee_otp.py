from django.db import models

class EmployeeOTP(models.Model):
    mobile_number = models.CharField(max_length=10, null=False)
    otp = models.CharField(max_length=6, null=False)
    generated_time = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        db_table = "employee_otp"
        verbose_name = "employee_otp"