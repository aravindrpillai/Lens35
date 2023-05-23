from django.db import models
from .employee_bank_details import EmployeeBankDetails

class Employees(models.Model):
    employee_id = models.UUIDField(unique=True)
    full_name = models.CharField(max_length=100, null=True)
    mobile_number = models.CharField(max_length=10, null=False, unique=True)
    
    profile_name = models.CharField(max_length=50, null=True, unique=True)

    email_id = models.EmailField(null=True, unique=True)
    email_id_verified = models.BooleanField(default=False)
    
    subscribe_for_updates = models.BooleanField(default=True)
    profile_approved = models.BooleanField(default=False)

    display_picture = models.CharField(max_length=50, null=True, unique=True)
    id_proof_type = models.CharField(max_length=20, null=True, choices=(('aadhar', 'aadhar'), ('passport', 'passport'), ('driving_licence', 'driving_licence'),('voters_id', 'voters_id')))
    id_proof_front = models.CharField(max_length=50, null=True, unique=True)
    id_proof_back = models.CharField(max_length=50, null=True, unique=True)
    
    base_location_pincode = models.CharField(max_length=6, null=True)
    base_location_city = models.CharField(max_length=100, null=True)
    base_location_latitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)
    base_location_longitude = models.DecimalField(max_digits=15, decimal_places=12, null=True)

    portfolios = models.JSONField(null=True)

    is_photographer = models.BooleanField(null=False, default=False)
    is_videographer = models.BooleanField(null=False, default=False)
    is_drone_photographer = models.BooleanField(null=False, default=False)
    is_photo_editor = models.BooleanField(null=False, default=False)
    is_video_editor = models.BooleanField(null=False, default=False)

    #if below flag is true = means the user has not filled all information
    is_draft = models.BooleanField(null=False, default=True)


    #Employee Bank Info
    bank_info = models.ForeignKey(EmployeeBankDetails, null=True, on_delete=models.CASCADE)
    class Meta:
        db_table = "employees"
        verbose_name = "employees"