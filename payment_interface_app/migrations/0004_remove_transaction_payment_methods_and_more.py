# Generated by Django 5.1.7 on 2025-03-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_interface_app', '0003_alter_transaction_payment_methods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='payment_methods',
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
