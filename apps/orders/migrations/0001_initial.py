# Generated by Django 5.1.7 on 2025-04-19 10:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0003_alter_category_category_name'),
        ('vendor', '0004_oepeninghour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('country', models.CharField(blank=True, max_length=15)),
                ('city', models.CharField(max_length=15)),
                ('pin_code', models.CharField(max_length=10)),
                ('total', models.FloatField(max_length=10)),
                ('tax_data', models.JSONField(blank=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}", null=True)),
                ('total_data', models.JSONField(blank=True, null=True)),
                ('total_tax', models.FloatField()),
                ('payment_method', models.CharField(max_length=25)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('ACCEPTED', '  Accepted'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='NEW', max_length=15)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ManyToManyField(blank=True, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transection_id', models.CharField(max_length=255, unique=True)),
                ('payment_method', models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('PAYPAL', 'PayPal'), ('BANK_TRANSFER', 'Bank Transfer')], max_length=50)),
                ('amount', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderdFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fooditem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.fooditem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
    ]
