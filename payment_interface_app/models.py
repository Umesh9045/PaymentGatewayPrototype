from django.db import models
from payment_methods_app.models import Payment_Method
from payment_status_app.models import Payment_Status

class Transaction(models.Model):
    def get_payment_method_choices():
        return [(choices.id, choices.name) for choices in Payment_Method.objects.all()]
    
    def get_payment_status_choices():
        return [(choices.id, choices.name) for choices in Payment_Status.objects.all()]

    cart_amount = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255) 
    payment_status = models.CharField(max_length=25, default='3')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - OrderID {self.order_id}"
