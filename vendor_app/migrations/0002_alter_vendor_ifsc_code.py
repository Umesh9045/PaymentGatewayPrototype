# Generated by Django 5.1.7 on 2025-03-28 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='ifsc_code',
            field=models.CharField(max_length=11),
        ),
    ]
