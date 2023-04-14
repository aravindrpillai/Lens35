# Generated by Django 4.1.6 on 2023-03-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_employees', '0003_alter_employees_id_proof_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='id_proof_type',
            field=models.CharField(choices=[('aadhar', 'aadhar'), ('passport', 'passport'), ('driving_licence', 'driving_licence'), ('voters_id', 'voters_id')], max_length=20, null=True),
        ),
    ]
