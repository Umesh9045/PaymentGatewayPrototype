from django.test import TestCase, Client
from django.urls import reverse
from payment_interface_app.models import Transaction
from payment_methods_app.models import Payment_Method
from payment_status_app.models import Payment_Status
from vendor_app.models import Vendor

# ==============================
# Test Cases for Transaction Model
# ==============================
class TransactionModelTest(TestCase):

    def setUp(self):
        """Set up initial data for testing"""
        # Creating required Payment Method and Payment Status objects
        self.payment_method = Payment_Method.objects.create(name="Credit Card")
        self.payment_status = Payment_Status.objects.create(name="Completed")

    # -------------------------------
    # Test Case 1: Transaction Creation
    # -------------------------------
    def test_transaction_creation(self):
        """
        Run:
        - Creates a Transaction and checks if data is correctly stored and retrieved.

        Success:
        - When the transaction order_id, payment_method, and payment_status match the expected values.

        Failure:
        - If any field does not store or return the correct value.
        """
        transaction = Transaction.objects.create(
            cart_amount=1000.50,
            final_amount=950.00,
            vendor_id="Vendor123",
            order_id="Order123",
            payment_method=self.payment_method.name,
            payment_status=self.payment_status.name
        )

        self.assertEqual(transaction.order_id, "Order123")  # Expected order ID
        self.assertEqual(transaction.payment_method, "Credit Card")  # Expected payment method
        self.assertEqual(transaction.payment_status, "Completed")  # Expected payment status

    # -------------------------------
    # Test Case 2: Multiple Transactions
    # -------------------------------
    def test_multiple_transactions(self):
        """
        Run:
        - Creates multiple transactions and verifies if they are stored correctly.

        Success:
        - When the total count of transactions matches the expected number.

        Failure:
        - If the count is incorrect, meaning not all transactions were saved properly.
        """
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

        self.assertEqual(Transaction.objects.count(), 2)  # Expecting 2 transactions


# ==============================
# Test Cases for Transaction View
# ==============================
class TransactionViewTest(TestCase):

    def setUp(self):
        """Set up initial data for testing"""
        self.client = Client()

        # Create Vendor
        self.vendor = Vendor.objects.create(vendor_name="Test Vendor")

        # Create Payment Method
        self.payment_method = Payment_Method.objects.create(name="UPI")

        # Create Payment Status
        self.payment_status = Payment_Status.objects.create(name="Success")

        # Create Transaction
        self.transaction = Transaction.objects.create(
            cart_amount=500.00,
            final_amount=480.00,
            vendor_id=str(self.vendor.id),
            order_id="Order123",
            payment_method=str(self.payment_method.id),
            payment_status=str(self.payment_status.id),
        )

    # -------------------------------
    # Test Case 3: View Loads Successfully
    # -------------------------------
    def test_all_transactions_view_status_code(self):
        """
        Run:
        - Calls the `all_transactions` view and checks if it loads properly.

        Success:
        - If the response status code is 200.

        Failure:
        - If the response status code is anything other than 200 (e.g., 404 if the view URL is incorrect).
        """
        response = self.client.get(reverse('all_transactions'))  # Ensure URL pattern matches
        self.assertEqual(response.status_code, 200)

    # -------------------------------
    # Test Case 4: Transaction Data is Displayed Correctly
    # -------------------------------
    def test_all_transactions_view_content(self):
        """
        Run:
        - Calls the `all_transactions` view and checks if the correct transaction data is displayed.

        Success:
        - If the response contains the expected Order ID, Vendor Name, Payment Method, and Payment Status.

        Failure:
        - If any of these values are missing from the response.
        """
        response = self.client.get(reverse('all_transactions'))
        self.assertContains(response, "Order123")  # Checking if Order ID is displayed
        self.assertContains(response, "Test Vendor")  # Checking if Vendor name is displayed
        self.assertContains(response, "UPI")  # Checking if Payment Method name is displayed
        self.assertContains(response, "Success")  # Checking if Payment Status name is displayed
