
from vendors.models import PurchaseOrder
from vendors.serializers import PurchaseOrderSerializer
from .models import Vendor
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import PurchaseOrder, Vendor 
from .serializers import (
    PurchaseOrderSerializer,
    VendorSerializer,
    PurchaseOrderSerializer,
)

#POST /api/purchase_orders/ (Create Purchase Order):
def test_create_purchase_order_valid_data(self):
  """Tests creating a purchase order with valid data."""
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  data = {
      'vendor': vendor.pk,
      # ... other purchase order data 
  }
  url = reverse('purchaseorder-list')
  response = self.client.post(url, data, format='json')
  self.assertEqual(response.status_code, 201)
  self.assertEqual(PurchaseOrder.objects.count(), 1)
  self.assertEqual(response.data, PurchaseOrderSerializer(PurchaseOrder.objects.get()).data)

def test_create_purchase_order_missing_required_field(self):
  """Tests creating a purchase order with a missing required field."""
  data = {}  # Missing 'vendor' field
  url = reverse('purchaseorder-list')
  response = self.client.post(url, data, format='json')
  self.assertEqual(response.status_code, 400)
  self.assertEqual(PurchaseOrder.objects.count(), 0)
  self.assertIn('vendor', response.data)  # Check for error message on missing field

def test_create_purchase_order_invalid_foreign_key(self):
  """Tests creating a purchase order with an invalid foreign key."""
  data = {'vendor': 100}  # Non-existent vendor ID
  url = reverse('purchaseorder-list')
  response = self.client.post(url, data, format='json')
  self.assertEqual(response.status_code, 400)
  self.assertEqual(PurchaseOrder.objects.count(), 0)
  self.assertIn('vendor', response.data)  # Check for error message on invalid foreign key


#GET /api/purchase_orders/ (List All Purchase Orders):
def test_get_purchase_order_list_empty(self):
  """Tests retrieving a list of purchase orders when there are none."""
  url = reverse('purchaseorder-list')
  response = self.client.get(url)
  self.assertEqual(response.status_code, 200)
  self.assertEqual(response.data, [])

def test_get_purchase_order_list_multiple(self):
  """Tests retrieving a list of purchase orders with multiple entries."""
  vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='vendor1@example.com')
  vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='vendor2@example.com')
  purchase_order1 = PurchaseOrder.objects.create(vendor=vendor1)
  purchase_order2 = PurchaseOrder.objects.create(vendor=vendor2)
  url = reverse('purchaseorder-list')
  response = self.client.get(url)
  self.assertEqual(response.status_code, 200)
  self.assertEqual(len(response.data), 2)
  self.assertEqual(
      set(response.data[0].keys()), set(PurchaseOrderSerializer(purchase_order1).data.keys())
  )  # Verify data structure

def test_get_purchase_order_list_filtered(self):
  """Tests retrieving a list of purchase orders using filter parameters (if supported)."""
  # Adjust this test based on your API's filtering capabilities
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  purchase_order1 = PurchaseOrder.objects.create(vendor=vendor, status='pending')
  purchase_order2 = PurchaseOrder.objects.create(vendor=vendor, status='approved')


#PUT /api/purchase_orders/{po_id} (Update Purchase Order):
def test_update_purchase_order_valid_data(self):
  """Tests updating a purchase order with valid data."""
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  purchase_order = PurchaseOrder.objects.create(vendor=vendor)
  data = {'total_amount': 1000.00}  # Update total amount
  url = reverse('purchaseorder-detail', kwargs={'pk': purchase_order.pk})
  response = self.client.put(url, data, format='json')
  self.assertEqual(response.status_code, 200)
  self.assertEqual(PurchaseOrder.objects.get(pk=purchase_order.pk).total_amount, 1000.00)
  self.assertEqual(response.data, PurchaseOrderSerializer(PurchaseOrder.objects.get()).data)

def test_update_purchase_order_invalid_data(self):
  """Tests updating a purchase order with invalid data."""
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  purchase_order = PurchaseOrder.objects.create(vendor=vendor)
  data = {'invalid_field': 'invalid_value'}  # Non-existent field
  url = reverse('purchaseorder-detail', kwargs={'pk': purchase_order.pk})
  response = self.client.put(url, data, format='json')
  self.assertEqual(response.status_code, 400)
  # Check for error message on invalid field

def test_update_purchase_order_not_found(self):
  """Tests updating a non-existent purchase order."""
  data = {'total_amount': 1000.00}
  url = reverse('purchaseorder-detail', kwargs={'pk': 100})  # Non-existent ID
  response = self.client.put(url, data, format='json')
  self.assertEqual(response.status_code, 404)


#DELETE /api/purchase_orders/{po_id} (Delete Purchase Order):
def test_delete_purchase_order(self):
  """Tests deleting a purchase order."""
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  purchase_order = PurchaseOrder.objects.create(vendor=vendor)
  url = reverse('purchaseorder-detail', kwargs={'pk': purchase_order.pk})
  response = self.client.delete(url)
  self.assertEqual(response.status_code, 204)  # No content on successful deletion
  self.assertEqual(PurchaseOrder.objects.count(), 0)

def test_delete_purchase_order_not_found(self):
  """Tests deleting a non-existent purchase order."""
  url = reverse('purchaseorder-detail', kwargs={'pk': 100})  # Non-existent ID
  response = self.client.delete(url)
  self.assertEqual(response.status_code, 404)

#GET/api/vendors/{vendor_id}/ to retrieve a specific vendors details
def test_get_vendor_detail_valid(self):
  """Tests retrieving a specific vendor's details."""
  vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com')
  url = reverse('vendor-detail', kwargs={'pk': vendor.pk})
  response = self.client.get(url)
  self.assertEqual(response.status_code, 200)
  self.assertEqual(response.data, VendorSerializer(vendor).data)

def test_get_vendor_detail_not_found(self):
  """Tests retrieving a non-existent vendor."""
  url = reverse('vendor-detail', kwargs={'pk': 100})  # Non-existent ID
  response = self.client.get(url)
  self.assertEqual(response.status_code, 404)


