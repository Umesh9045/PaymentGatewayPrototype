from django.core.exceptions import ValidationError
from django.test import TestCase
from vendor_app.models import Vendor

class VendorModelTest(TestCase):

    def setUp(self):
        """Set up a valid Vendor instance for testing"""
        self.valid_vendor = Vendor.objects.create(
            vendor_name="Valid Vendor",
            vendor_type="OC",
            vendor_contact="9876543210",  # Valid contact number
            vendor_address="123 Main Street",
            bank_name="State Bank",
            ifsc_code="SBIN0001234",
            account_number="123456789012",
            fee_bearer="0",
        )

    def test_valid_vendor_creation(self):
        """Test that a vendor with valid data is successfully created"""
        self.assertEqual(self.valid_vendor.vendor_name, "Valid Vendor")
        self.assertEqual(self.valid_vendor.vendor_contact, "9876543210")

    def test_invalid_contact_number(self):
        """Test validation for an invalid vendor contact number"""
        vendor = Vendor(
            vendor_name="Test Vendor",
            vendor_type="OC",
            vendor_contact="1234",  # Invalid: Should be 10 digits
            vendor_address="Test Address",
            bank_name="Test Bank",
            ifsc_code="TEST1234567",
            account_number="123456789",
            fee_bearer="1",
        )

        # Call full_clean() to trigger field validation
        with self.assertRaises(ValidationError) as context:
            vendor.full_clean()

        # Ensure correct validation error message
        self.assertIn("Enter a valid 10-digit mobile number.", str(context.exception))
