# Generated by Django 4.1.6 on 2023-05-27 11:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apps_bookings', '0004_serviceinvoiceitems_invoice_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='file_id',
            field=models.UUIDField(default=uuid.UUID('9724c382-224d-45b6-b39e-5735268637a6')),
        ),
    ]
