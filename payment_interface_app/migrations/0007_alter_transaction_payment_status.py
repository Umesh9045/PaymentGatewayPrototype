# Generated by Django 5.1.7 on 2025-03-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_interface_app', '0006_alter_transaction_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_status',
            field=models.CharField(default='3', max_length=25),
        ),
    ]
