# Generated by Django 5.0.3 on 2024-04-01 17:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_bookings', '0009_alter_files_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_id',
            field=models.UUIDField(default=uuid.UUID('bd1bb33a-1d61-4ed1-820d-a1088243decd')),
        ),
    ]
