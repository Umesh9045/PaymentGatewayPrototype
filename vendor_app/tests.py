from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from django.test import Client
from .models import Vendor

@pytest.mark.django_db  # Marks test to use the database
def test_vender_manage_view():
    client = Client()

    # Create test vendors
    vendor1 = Vendor.objects.create(name="Vendor A")
    vendor2 = Vendor.objects.create(name="Vendor B")

    # Send request to view
    response = client.get(reverse('vender_manage'))  # Ensure URL name is correct

    # Assertions
    assert response.status_code == 200  # Check if the view returns 200 OK
    assert 'vendors' in response.context  # Ensure 'vendors' is passed to the template
    assert list(response.context['vendors']) == [vendor1, vendor2]  # Verify vendors list

    # Check if the correct template is used
    templates_used = [template.name for template in response.templates]
    assert 'manage.html' in templates_used
