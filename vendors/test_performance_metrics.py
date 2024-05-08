import pytest
from vendors.models import PerformanceMetric
from vendors.serializers import PerformanceMetricSerializer , VendorSerializer, PurchaseOrderSerializer
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Vendor, PurchaseOrder

#GET /api/vendors/{vendor_id}/performance:
def test_get_vendor_performance_valid(self):
  """Tests retrieving a vendor's performance (implementation dependent)."""
  # calculating and retrieving performance data.
  vendor = Vendor.objects.create(name='Test Vendor', email='test@example.com')
  # Simulate performance data 
  performance_data = {'on_time_delivery': 0.9, 'average_response_time': 2}
  url = reverse('vendor-performance', kwargs={'pk': vendor.pk})
  response = self.client.get(url)
  self.assertEqual(response.status_code, 200)
  self.assertEqual(response.data, performance_data)

def test_get_vendor_performance_not_found(self):
  """Tests retrieving performance for a non-existent vendor."""
  url = reverse('vendor-performance', kwargs={'pk': 100})  # Non-existent ID
  response = self.client.get(url)
  self.assertEqual(response.status_code, 404)

#POST /api/purchase_orders/{po_id}/acknowledge:
def test_acknowledge_purchase_order_valid(self):
  """Tests acknowledging a purchase order."""
  vendor = Vendor.objects.create(name='Test Vendor', email='test@example.com')
  purchase_order = PurchaseOrder.objects.create(vendor=vendor, status='pending')
  url = reverse('purchaseorder-acknowledge', kwargs={'pk': purchase_order.pk})
  response = self.client.post(url, format='json')  # Assuming no data needed
  self.assertEqual(response.status_code, 200)
  # Check if purchase order status is updated (e.g., 'acknowledged')
  self.assertEqual(PurchaseOrder.objects.get(pk=purchase_order.pk).status, 'acknowledged')  # Adjust status as needed

def test_acknowledge_purchase_order_not_found(self):
  """Tests acknowledging a non-existent purchase order."""
  url = reverse('purchaseorder-acknowledge', kwargs={'pk': 100})  # Non-existent ID
  response = self.client.post(url, format='json')
  self.assertEqual(response.status_code, 404)

def test_acknowledge_purchase_order_invalid_status(self):
  """Tests acknowledging a purchase order with an invalid status (optional)."""
  # If applicable, test if acknowledging is allowed only for specific purchase order statuses.
  vendor = Vendor.objects.create(name='Test Vendor', email='test@example.com')
  purchase_order = PurchaseOrder.objects.create(vendor=vendor, status='completed')
  url = reverse('purchaseorder-acknowledge', kwargs={'pk': purchase_order.pk})
  response = self.client.post(url, format='json')
  self.assertEqual(response.status_code, 400)  
  self.assertIn('status', response.data)  

@pytest.mark.django_db
def test_create_performance_metric(vendor, metric_data):
    metric_data['vendor'] = vendor.pk
    serializer = PerformanceMetricSerializer(data=metric_data)
    assert serializer.is_valid()
    serializer.save()
    metric = PerformanceMetric.objects.get(criteria=metric_data['criteria'])
    assert metric.vendor.pk == vendor.pk
    assert metric.score == metric_data['score']

@pytest.mark.django_db
def test_create_performance_metric_missing_vendor(metric_data):
    del metric_data['vendor']
    serializer = PerformanceMetricSerializer(data=metric_data)
    assert not serializer.is_valid()
    assert 'vendor' in serializer.errors

def test_retrieve_performance_metric(self, performance_metric):
    response = self.client.get(f'/performance-metrics/{performance_metric.pk}/')
    assert response.status_code == 200
    data = response.json()
    assert data['criteria'] == performance_metric.criteria
    assert data['score'] == performance_metric.score

def test_retrieve_nonexistent_performance_metric(self):
    response = self.client.get('/performance-metrics/9999/')
    assert response.status_code == 404

def test_update_performance_metric(self, performance_metric):
    data = {'score': 80.0}  # Update score
    response = self.client.put(f'/performance-metrics/{performance_metric.pk}/', data=data)
    assert response.status_code == 200
    performance_metric.refresh_from_db()
    assert performance_metric.score == data['score']

def test_update_performance_metric_invalid_data(self, performance_metric):
    data = {'invalid_field': 'invalid value'}
    response = self.client.put(f'/performance-metrics/{performance_metric.pk}/', data=data)
    assert response.status_code == 400

def test_delete_performance_metric(self, performance_metric):
    response = self.client.delete(f'/performance-metrics/{performance_metric.pk}/')
    assert response.status_code == 204
    assert not PerformanceMetric.objects.filter(pk=performance_metric.pk).exists()

@pytest.mark.django_db
def test_delete_nonexistent_performance_metric(self):
    response = self.client.delete('/performance-metrics/9999/')
    assert response.status_code == 404
