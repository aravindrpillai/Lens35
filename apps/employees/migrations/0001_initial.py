# Generated by Django 4.1.6 on 2023-03-14 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=10)),
                ('otp', models.CharField(max_length=6)),
                ('generated_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'employee_otp',
                'db_table': 'employee_otp',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.UUIDField(unique=True)),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('mobile_number', models.CharField(max_length=10, unique=True)),
                ('email_id', models.EmailField(max_length=254, null=True, unique=True)),
                ('email_id_verified', models.BooleanField(default=False)),
                ('subscribe_for_updates', models.BooleanField(default=True)),
                ('profile_approved', models.BooleanField(default=False)),
                ('display_picture', models.UUIDField(null=True, unique=True)),
                ('id_proof_type', models.CharField(choices=[('A', 'Aadhar'), ('P', 'Passport'), ('D', 'DrivingLicence'), ('V', 'VotersID')], max_length=15, null=True)),
                ('id_proof_front', models.UUIDField(null=True, unique=True)),
                ('id_proof_back', models.UUIDField(null=True, unique=True)),
                ('base_location_pincode', models.CharField(max_length=6, null=True)),
                ('base_location_city', models.CharField(max_length=100, null=True)),
                ('portfolios', models.JSONField(null=True)),
                ('is_photographer', models.BooleanField(default=False)),
                ('is_videographer', models.BooleanField(default=False)),
                ('is_drone_photographer', models.BooleanField(default=False)),
                ('is_photo_editor', models.BooleanField(default=False)),
                ('is_video_editor', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'employees',
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='EmployeeToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=10)),
                ('employee_id', models.UUIDField()),
                ('device_id', models.UUIDField()),
                ('token', models.UUIDField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('keep_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'employee_token',
                'managed': True,
                'unique_together': {('mobile_number', 'device_id', 'token')},
            },
        ),
    ]
