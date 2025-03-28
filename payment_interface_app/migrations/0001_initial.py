# Generated by Django 5.1.7 on 2025-03-27 07:00

import payment_interface_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('final_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vendor_id', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('payment_methods', models.CharField(choices=payment_interface_app.models.Transaction.get_payment_method_choices, max_length=20)),
                ('payment_status', models.CharField(choices=[('0', 'Fail'), ('1', 'Success'), ('2', 'Pending')], default='2', max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
