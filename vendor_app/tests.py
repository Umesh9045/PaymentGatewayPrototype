from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from vendor_app.models import Vendor

class VendorModelTest(TestCase):

    def setUp(self):
        """
        # Test case 1 - Vendor Creation with Valid Data
        # success - when a vendor is created successfully
        # fail - when vendor creation fails
        """
        self.valid_vendor = Vendor.objects.create(
            vendor_name="Valid Vendor",
            vendor_type="OC",
            vendor_contact="9876543210",  # Valid 10-digit number
            vendor_address="123 Main Street",
            bank_name="State Bank",
            ifsc_code="SBIN0001234",
            account_number="123456789012",
            fee_bearer="0",
        )

    def test_valid_vendor_creation(self):
        """
        # Test case 2 - Vendor Name and Contact Validation
        # success - when vendor name and contact match expected values
        # fail - when they do not match
        """
        self.assertEqual(self.valid_vendor.vendor_name, "Valid Vendor")
        self.assertEqual(self.valid_vendor.vendor_contact, "9876543210")

    def test_invalid_contact_number(self):
        """
        # Test case 3 - Vendor Contact Number Validation
        # success - when validation error is raised for an invalid contact number
        # fail - when validation unexpectedly passes
        """
        vendor = Vendor(
            vendor_name="Test Vendor",
            vendor_type="OC",
            vendor_contact="1234",  # Invalid: Less than 10 digits
            vendor_address="Test Address",
            bank_name="Test Bank",
            ifsc_code="TEST1234567",
            account_number="123456789",
            fee_bearer="1",
        )

        # Trigger field validation
        with self.assertRaises(ValidationError) as context:
            vendor.full_clean()

        # Check for the expected validation error message
        self.assertIn("Enter a valid 10-digit mobile number.", str(context.exception))


class VendorViewTest(TestCase):

    def setUp(self):
        """
        # Test case 1 - Setup Vendor Data
        # success - when vendors are successfully created
        # fail - when vendor creation fails
        """
        self.client = Client()
        self.vendor1 = Vendor.objects.create(
            vendor_name="Vendor One",
            vendor_type="OC",
            vendor_contact="9876543210",
            vendor_address="123 Market Street",
            bank_name="Test Bank",
            ifsc_code="TEST1234567",
            account_number="123456789012",
            fee_bearer="0",
        )
        self.vendor2 = Vendor.objects.create(
            vendor_name="Vendor Two",
            vendor_type="KS",
            vendor_contact="8765432109",
            vendor_address="456 Grocery Lane",
            bank_name="Another Bank",
            ifsc_code="ANBK1234567",
            account_number="987654321098",
            fee_bearer="1",
        )

    def test_vendor_manage_view_status_code(self):
        """
        # Test case 2 - Vendor Management View Response Code
        # success - when the response status code is 200
        # fail - when the response status code is not 200
        """
        response = self.client.get(reverse('all_vendors'))  # Updated to match urls.py
        self.assertEqual(response.status_code, 200)

    def test_vendor_manage_view_content(self):
        """
        # Test case 3 - Vendor Management View Content
        # success - when both vendor names appear in the response
        # fail - when one or both vendor names are missing
        """
        response = self.client.get(reverse('all_vendors'))  # Updated to match urls.py
        self.assertContains(response, "Vendor One")
        self.assertContains(response, "Vendor Two")
