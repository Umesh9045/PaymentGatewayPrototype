from django.test import TestCase, Client
from django.urls import reverse
from payment_interface_app.models import Transaction
from payment_methods_app.models import Payment_Method
from vendor_app.models import Vendor
import json
from decimal import Decimal

class PaymentInterfaceViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test payment methods
        self.payment_method = Payment_Method.objects.create(name="Credit Card")

        # Create a test vendor with fee_bearer = 1
        self.vendor = Vendor.objects.create(
            vendor_name="Valid Vendor",
            vendor_type="OC",
            vendor_contact="9876543210",
            vendor_address="123 Main Street",
            bank_name="State Bank",
            ifsc_code="SBIN0001234",
            account_number="123456789012",
            fee_bearer=1,
            payment_methods=[self.payment_method.id]  # Storing as list
        )

        self.order_id = "101"
        self.checkout_amount = Decimal("1000.00")
        self.payment_handling_charges = (Decimal("2.00") / Decimal("100.00")) * self.checkout_amount
        self.gst_on_payment_handling = (Decimal("18.00") / Decimal("100.00")) * self.payment_handling_charges
        self.final_amount = self.checkout_amount + self.payment_handling_charges + self.gst_on_payment_handling

    # Test case 1: Vendor not found
    # Success: When the API returns a 404 response for a non-existing vendor
    # Fail: When the API does not return a 404 response for a non-existing vendor
    def test_vendor_not_found(self):
        response = self.client.get(reverse("make_payment", args=[9999, self.order_id, str(self.checkout_amount)]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), "Payment Denied - Vendor not found")

    # Test case 2: Make payment with fee_bearer = 1
    # Success: When the final amount is correctly calculated and returned
    # Fail: When the final amount is incorrect or missing in response
    def test_make_payment_with_fee_bearer_1(self):
        response = self.client.get(reverse("make_payment", args=[self.vendor.id, self.order_id, str(self.checkout_amount)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vendor_name"], "Valid Vendor")
        self.assertEqual(
            Decimal(response.context["final_amount"]).quantize(Decimal("0.00")),
            self.final_amount.quantize(Decimal("0.00"))
        )

    # Test case 3: Make payment with fee_bearer = 0
    # Success: When the final amount equals the checkout amount (no additional charges)
    # Fail: When the final amount includes handling charges despite fee_bearer = 0
    def test_make_payment_with_fee_bearer_0(self):
        self.vendor.fee_bearer = 0
        self.vendor.save()
        response = self.client.get(reverse("make_payment", args=[self.vendor.id, self.order_id, str(self.checkout_amount)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.context["final_amount"]), self.checkout_amount)

    # Test case 4: Transaction already exists
    # Success: When the API denies duplicate payment request
    # Fail: When the API allows duplicate transactions
    def test_transaction_already_exists(self):
        Transaction.objects.create(
            vendor_id=self.vendor.id,
            order_id=self.order_id,
            cart_amount=self.checkout_amount,
            final_amount=self.final_amount,
            payment_status='1'  # Simulating a completed transaction
        )
        response = self.client.get(reverse("make_payment", args=[self.vendor.id, self.order_id, str(self.checkout_amount)]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payment Denied - Duplicate Request")

    # Test case 5: Transaction creation and fetching
    # Success: When a new transaction is successfully created and fetched
    # Fail: When the transaction is not created or incorrect details are stored
    def test_transaction_creation_and_fetching(self):
        response = self.client.get(reverse("make_payment", args=[self.vendor.id, self.order_id, str(self.checkout_amount)]))
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(vendor_id=self.vendor.id, order_id=self.order_id)
        self.assertEqual(transaction.cart_amount, self.checkout_amount)
        self.assertEqual(transaction.final_amount, self.final_amount)

class PaymentStatusUpdateTest(TestCase):
    def setUp(self):
        # Create test payment methods
        self.payment_method = Payment_Method.objects.create(name="Credit Card")

        # Create a test vendor with fee_bearer = 1
        self.vendor = Vendor.objects.create(
            vendor_name="Valid Vendor",
            vendor_type="OC",
            vendor_contact="9876543210",
            vendor_address="123 Main Street",
            bank_name="State Bank",
            ifsc_code="SBIN0001234",
            account_number="123456789012",
            fee_bearer=1,
            payment_methods=[self.payment_method.id]  # Storing as list
        )

        response = self.client.get(reverse("make_payment", args=[self.vendor.id, '1', '100']))
        self.assertEqual(response.status_code, 200)
        self.transaction = Transaction.objects.get(vendor_id=self.vendor.id, order_id='1')

    # Test case 6: Transaction not found
    # Success: When the API returns 404 for a non-existing transaction
    # Fail: When the API does not return 404
    def test_transaction_not_found(self):
        response = self.client.get(reverse("update_payment", args=[9999, self.payment_method.id, 1]))
        self.assertEqual(response.status_code, 404)

    # Test case 7: Duplicate payment request
    # Success: When the API correctly processes the duplicate request
    # Fail: When the API fails to handle duplicate requests
    def test_duplicate_payment_request(self):
        response = self.client.get(reverse("update_payment", args=[self.transaction.id, self.payment_method.id, 1]))
        self.assertEqual(response.status_code, 200)

    # Test case 8: Invalid payment method
    # Success: When the API returns 400 for an invalid payment method
    # Fail: When the API does not return 400
    def test_invalid_payment_method(self):
        response = self.client.get(reverse("update_payment", args=[self.transaction.id, 9999, 1]))
        self.assertEqual(response.status_code, 404)

    # Test case 9: Bad payment request
    # Success: When the API returns 400 for an invalid payment status
    # Fail: When the API allows an invalid payment status
    def test_bad_payment_request(self):
        response = self.client.get(reverse("update_payment", args=[self.transaction.id, self.payment_method.id, 3]))
        self.assertEqual(response.status_code, 404)

    # Test case 10: Successful payment update with status 1
    # Success: When the API successfully updates the payment status to 1
    # Fail: When the API fails to update the status
    def test_successful_payment_update_status_1(self):
        response = self.client.get(reverse("update_payment", args=[self.transaction.id, self.payment_method.id, 1]))
        self.assertEqual(response.status_code, 200)

    # Test case 11: Successful payment update with status 2
    # Success: When the API successfully updates the payment status to 2
    # Fail: When the API fails to update the status
    def test_successful_payment_update_status_2(self):
        response = self.client.get(reverse("update_payment", args=[self.transaction.id, self.payment_method.id, 2]))
        self.assertEqual(response.status_code, 200)