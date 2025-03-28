import re
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from payment_methods_app.models import Payment_Method

class Vendor(models.Model):
    # Choices for Vendor Type
    VENDOR_TYPE_CHOICES = [
        ('KS', 'Kirana Shop'),
        ('OC', 'Online Commerce'),
        ('RE', 'Restaurant'),
        ('OT', 'Other'),
    ]

    # Choices for Fee Bearer
    FEE_BEARER_CHOICES = [
        ('0', 'Vendor Pays'),
        ('1', 'Customer Pays'),
    ]

    def get_payment_method_choices():
        return [(choices.id, choices.name) for choices in Payment_Method.objects.all()] or [('default', 'No Payment Methods')]

    vendor_name = models.CharField(max_length=255)

    vendor_type = models.CharField(
        max_length=2,
        choices=VENDOR_TYPE_CHOICES,
        default='OT'
    )

    vendor_contact = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid 10-digit mobile number."
            )
        ]
    )

    vendor_website = models.URLField(blank=True, null=True)
    vendor_address = models.TextField()
    bank_name = models.CharField(max_length=255)

    ifsc_code = models.CharField(
        max_length=11
    )

    account_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d{9,18}$',
                message="Enter a valid bank account number (9-18 digits)."
            )
        ]
    )

    # payment_methods = MultiSelectField(choices=PAYMENT_METHOD_CHOICES, max_length=20)
    payment_methods = MultiSelectField(choices=get_payment_method_choices, max_length=20)

    fee_bearer = models.CharField(
        max_length=1,
        choices=FEE_BEARER_CHOICES,
        default='0'
    )

    onboarding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor_name} ({self.get_vendor_type_display()}) - Payment: {', '.join(self.payment_methods)}"
    