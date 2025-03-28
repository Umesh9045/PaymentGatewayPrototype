# Generated by Django 5.1.7 on 2025-03-27 07:08

import payment_interface_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_interface_app', '0002_alter_transaction_payment_methods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_methods',
            field=models.CharField(choices=payment_interface_app.models.Transaction.get_payment_method_choices, max_length=20),
        ),
    ]
