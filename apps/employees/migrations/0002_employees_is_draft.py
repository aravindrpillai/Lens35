# Generated by Django 4.1.6 on 2023-05-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]