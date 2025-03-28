from django.test import TestCase
from payment_status_app.models import Payment_Status

class PaymentStatusModelTest(TestCase):

    # Test case 1 - Payment_Status model should store and retrieve name correctly.
    # Test case 1 - Run (success = when name is correctly stored and retrieved, fail = when name retrieval is incorrect or empty)
    def test_payment_status_creation(self):
        """Test if Payment_Status model correctly stores and retrieves name"""
        status = Payment_Status.objects.create(name="Pending")
        self.assertEqual(status.name, "Pending")

    # Test case 2 - Ensuring multiple Payment_Status objects are stored correctly.
    # Test case 2 - Run (success = when multiple statuses are stored and retrieved correctly, fail = when incorrect data is retrieved)
    def test_multiple_payment_statuses(self):
        """Test if multiple Payment_Status objects can be created and retrieved correctly"""
        status1 = Payment_Status.objects.create(name="Completed")
        status2 = Payment_Status.objects.create(name="Failed")
        
        self.assertEqual(Payment_Status.objects.count(), 2)
        self.assertIn(status1, Payment_Status.objects.all())
        self.assertIn(status2, Payment_Status.objects.all())
