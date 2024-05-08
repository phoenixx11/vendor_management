from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Vendor  
from .serializers import VendorSerializer  


class VendorAPITestCase(APITestCase):

    def test_create_vendor(self):
        """
        Test creating a new vendor with valid data.
        """
        url = reverse('vendor-list')  
        data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            # Add other relevant fields as needed
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # Check for successful creation (201 Created)
        self.assertEqual(Vendor.objects.count(), 1)  # Verify a new vendor is created
        self.assertEqual(response.data, VendorSerializer(Vendor.objects.get()).data)  # Verify data matches serialized response

    def test_create_vendor_invalid_data(self):
        """
        Test creating a vendor with missing required field.
        """
        url = reverse('vendor-list')
        data = {'contact_details': 'test@example.com'}  # Missing 'name' field
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Check for bad request (400)
        self.assertEqual(Vendor.objects.count(), 0)  # Verify no vendor is created
        self.assertIn('name', response.data)  # Check for error message on missing field

    def test_create_vendor_duplicate_email(self):
        """
        Test creating a vendor with a duplicate email.
        """
        vendor = Vendor.objects.create(name='Existing Vendor', contact_details='test@example.com')
        url = reverse('vendor-list')
        data = {'name': 'Duplicate Vendor', 'contact_details': vendor.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Check for bad request (400)
        self.assertEqual(Vendor.objects.count(), 1)  # Verify no new vendor is created
        self.assertIn('contact_details', response.data)  # Check for error message on duplicate email


class VendorAPITestCase(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')


    def test_get_vendor_list(self):
        """
        Test retrieving a list of vendors.
        """
        url = reverse('vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Check for successful retrieval (200 OK)
        self.assertEqual(len(response.data), 1)  # Verify one vendor is returned
        self.assertEqual(response.data[0], VendorSerializer(self.vendor).data)  # Verify data matches serialized response

    def test_get_vendor_detail(self):
        """
        Test retrieving a specific vendor by ID.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Check for successful retrieval (200 OK)
        self.assertEqual(response.data, VendorSerializer(self.vendor).data)  # Verify data matches serialized response

    def test_get_vendor_detail_not_found(self):
        """
        Test retrieving a non-existent vendor.
        """
        url = reverse('vendor-detail', kwargs={'pk': 100})  # Assuming ID doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Check for not found (404)

    def test_update_vendor(self):
        """
        Test updating a vendor with valid data.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        data = {'name': 'Updated Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.vendor.refresh_from_db()  # Refresh vendor object from database
        self.assertEqual(self.vendor.name, data['name'])  # Verify data is updated
        self.assertEqual(response.data, VendorSerializer(self.vendor).data)  # Verify data matches serialized response

    def test_update_vendor_invalid_data(self):
        """
        Test updating a vendor with missing required field.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        data = {}  # Missing 'name' field
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Check for bad request (400)
        self.vendor.refresh_from_db()  # Refresh vendor object from database
        self.assertEqual(self.vendor.name, 'Test Vendor')  # Verify data remains unchanged
        self.assertIn('name', response.data)  # Check for error message on missing field

    def test_delete_vendor(self):
        """
        Test deleting a vendor.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # Check for successful deletion (204 No Content)
        self.assertEqual(Vendor.objects.count(), 0)  # Verify vendor is deleted

    def test_delete_vendor_not_found(self):
        """
        Test deleting a non-existent vendor.
        """
        url = reverse('vendor-detail', kwargs={'pk': 100})  # Assuming ID doesn't exist
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

