# Generated by Django 5.1.7 on 2025-04-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_vendor_order_vendors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('SSL_COMMERZ', 'SSL Commerz'), ('PAYPAL', 'PayPal'), ('BANK_TRANSFER', 'Bank Transfer')], max_length=200),
        ),
    ]
