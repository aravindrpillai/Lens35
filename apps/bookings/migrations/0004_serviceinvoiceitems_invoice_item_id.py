# Generated by Django 4.1.6 on 2023-05-14 13:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apps_bookings', '0003_serviceinvoiceitems_delete_serviceinvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinvoiceitems',
            name='invoice_item_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
