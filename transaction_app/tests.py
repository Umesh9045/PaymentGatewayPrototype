from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from payment_interface_app.models import Transaction
from payment_methods_app.models import Payment_Method
from payment_status_app.models import Payment_Status

class TransactionModelTest(TestCase):

    def setUp(self):
        """Set up initial data for testing"""
        self.payment_method = Payment_Method.objects.create(name="Credit Card")
        self.payment_status = Payment_Status.objects.create(name="Completed")

    def test_transaction_creation(self):
        """Test if Transaction model correctly stores and retrieves data"""
        transaction = Transaction.objects.create(
            cart_amount=1000.50,
            final_amount=950.00,
            vendor_id="Vendor123",
            order_id="Order123",
            payment_method=self.payment_method.name,
            payment_status=self.payment_status.name
        )
        self.assertEqual(transaction.order_id, "Order123")
        self.assertEqual(transaction.payment_method, "Credit Card")
        self.assertEqual(transaction.payment_status, "Completed")

    def test_multiple_transactions(self):
        """Test if multiple transactions can be stored and counted correctly"""
        Transaction.objects.create(
            cart_amount=500.00,
            final_amount=480.00,
            vendor_id="Vendor001",
            order_id="Order001",
            payment_method=self.payment_method.name,
            payment_status=self.payment_status.name
        )
        Transaction.objects.create(
            cart_amount=1500.75,
            final_amount=1400.00,
            vendor_id="Vendor002",
            order_id="Order002",
            payment_method=self.payment_method.name,
            payment_status=self.payment_status.name
        )

        self.assertEqual(Transaction.objects.count(), 2)
