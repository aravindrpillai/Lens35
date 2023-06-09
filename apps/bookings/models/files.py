from apps.bookings.models.services import Services
from django.db import models
import uuid

class Files(models.Model):

    file_id = models.UUIDField(null=False, default=uuid.uuid4())
    service = models.ForeignKey(Services, null=False, on_delete=models.CASCADE)
    created_time = models.DateTimeField(null=False, auto_now_add=True)
    file_name = models.CharField(max_length=100, null=False)
    mime_type = models.CharField(max_length=25, null=False)

    class Meta:
        db_table = "files"
        verbose_name = "files"