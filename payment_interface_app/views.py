from django.http import HttpResponse
from django.shortcuts import render
from payment_methods_app.models import Payment_Method
from vendor_app.models import Vendor
from .models import Transaction

import pdb

# Create your views here.
def make_payment(request, vendor_id, order_id, checkout_amount):
    try:
        # Fetch vendor details
        vendor = Vendor.objects.get(id=vendor_id)

        payment_handling_charges = 0
        gst_on_payment_handling = 0
        checkout_amount = float(checkout_amount)
        final_amount = checkout_amount

        if int(vendor.fee_bearer) == 1:
            payment_handling_charges = (2 / 100) * checkout_amount  # 2% of checkout_amount
            gst_on_payment_handling = (18 / 100) * payment_handling_charges  # 18% of handling charges
            final_amount = checkout_amount + payment_handling_charges + gst_on_payment_handling  # Total payable amount

        # Get or create a transaction
        transaction, created = Transaction.objects.get_or_create(
            vendor_id=vendor_id,
            order_id=order_id,
            defaults={
                "cart_amount": checkout_amount,
                "final_amount": final_amount
            }
        )

        if transaction.cart_amount != checkout_amount:
            return HttpResponse("Payment Denied - Another payment in progress", status=404)
        
        # pdb.set_trace()

        if transaction.payment_status == '1' or transaction.payment_status == '2':
            return HttpResponse("Payment Denied - Duplicate Request", status=400)
    
        # Fetch payment method IDs from vendor
        payment_ids = vendor.payment_methods  # Assuming MultiSelectField stores IDs as a list
        
        # Fetch payment method names
        payment_methods_dict = {
            method.id: method.name
            for method in Payment_Method.objects.filter(id__in=payment_ids)
        }
        context = {
            "vendor_name": vendor.vendor_name,
            "vendor_contact": vendor.vendor_contact,
            "payment_options": payment_methods_dict,
            "order_id": transaction.order_id,
            "checkout_amount": transaction.cart_amount,
            "payment_handling_charges": payment_handling_charges,
            "gst_on_payment_handling": gst_on_payment_handling,
            "final_amount": transaction.final_amount,
            "payment_status": transaction.payment_status,
            "transaction_id": transaction.id,
        }
        print(context)
        return render(request, "make_payment.html", context)

    except Vendor.DoesNotExist:
        return HttpResponse("Payment Denied - Vendor not found", status=404)

def payment_status_update(request, transaction_id, payment_method_id, payment_status):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        
        #if payment status = fail or success
        if transaction.payment_status == '1' or transaction.payment_status == '2':
            return HttpResponse("Payment Denied - Duplicate Request", status=400)

        if payment_status == 3:
            return HttpResponse("Payment Denied - Invalid Payment Status", status=404)
        if payment_status == 2:
            transaction.payment_status = '2'
        if payment_status == 1:
            transaction.payment_status = '1'

        try:
            payment_method_obj = Payment_Method.objects.get(id=payment_method_id)
            payment_method_name = payment_method_obj.name  # Get the name
        except Payment_Method.DoesNotExist:
            return HttpResponse("Payment Denied - Invalid Payment Method", status=404)
        
        transaction.payment_method = str(payment_method_id)
        transaction.save()

        vendor = Vendor.objects.get(id = transaction.vendor_id)

        context = {
                'vendor_name' : vendor.vendor_name,
                'vendor_contact' : vendor.vendor_contact,
                'payment_options': payment_method_name,
                'order_id' : transaction.order_id,
                'checkout_amount' : transaction.cart_amount,
                'payment_handling_charges' : '0',
                'gst_on_payment_handling' : '0',
                'final_amount' : transaction.final_amount,
                'payment_status' : transaction.payment_status
            }
        
        return render(request, 'make_payment.html', context)

    except Transaction.DoesNotExist:
        return HttpResponse("Payment Denied - Transaction not found", status=404)


