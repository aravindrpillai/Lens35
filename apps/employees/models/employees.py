from django.db import models

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
    id_proof_type = models.CharField(max_length=15, null=True, choices=(('A', 'Aadhar'), ('P', 'Passport'), ('D', 'DrivingLicence'),('V', 'VotersID')))
    id_proof_front = models.CharField(max_length=50, null=True, unique=True)
    id_proof_back = models.CharField(max_length=50, null=True, unique=True)
    
    base_location_pincode = models.CharField(max_length=6, null=True)
    base_location_city = models.CharField(max_length=100, null=True)

    portfolios = models.JSONField(null=True)

    is_photographer = models.BooleanField(null=False, default=False)
    is_videographer = models.BooleanField(null=False, default=False)
    is_drone_photographer = models.BooleanField(null=False, default=False)
    is_photo_editor = models.BooleanField(null=False, default=False)
    is_video_editor = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "employees"
        verbose_name = "employees"