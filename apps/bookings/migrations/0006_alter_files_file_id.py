# Generated by Django 5.0.3 on 2024-04-01 16:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_bookings', '0005_files_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_id',
            field=models.UUIDField(default=uuid.UUID('3376b406-f8bc-4ae5-90d6-f81b4727aa84')),
        ),
    ]
