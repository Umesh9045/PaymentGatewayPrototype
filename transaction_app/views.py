from django.shortcuts import render
from payment_interface_app.models import Transaction
from vendor_app.models import Vendor
from payment_methods_app.models import Payment_Method
from payment_status_app.models import Payment_Status

# Create your views here.
def all_transactions(request):
    transactions = Transaction.objects.all()

    # Fetch all vendors and payment methods
    vendors = {str(vendor.id): vendor.vendor_name for vendor in Vendor.objects.all()} 
    payment_methods = {str(pm.id): pm.name for pm in Payment_Method.objects.all()}  # Ensure keys are strings
    payment_status = {str(status.id): status.name for status in Payment_Status.objects.all()}

    # Process transactions to replace IDs with names
    for transaction in transactions:
        transaction.vendor_id = vendors.get(str(transaction.vendor_id), "Unknown Vendor")
        transaction.payment_method = payment_methods.get(transaction.payment_method, "Unknown Method")
        transaction.payment_status = payment_status.get(transaction.payment_status, 'NA')

    return render(request, 'all_transactions.html', {'transactions': transactions})

