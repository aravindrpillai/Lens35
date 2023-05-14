# Generated by Django 4.1.6 on 2023-05-14 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps_bookings', '0002_services_closed_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceInvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_category', models.CharField(choices=[('booking_cost', 'booking_cost'), ('cancellation_charge', 'cancellation_charge'), ('discount', 'discount')], max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps_bookings.services')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apps_bookings.transactions')),
            ],
            options={
                'verbose_name': 'service_invoice_items',
                'db_table': 'service_invoice_items',
            },
        ),
        migrations.DeleteModel(
            name='ServiceInvoice',
        ),
    ]