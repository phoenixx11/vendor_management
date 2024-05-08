
from django.urls import path, include
from rest_framework import routers
from vendors import views
from vendors.views import VendorPerformanceView


router=routers.DefaultRouter()
router.register(r'vendors', views.VendorViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'performance-metrics', views.PerformanceMetricViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Vendor Endpoints
    path('vendors/', views.VendorViewSet.as_view({'get': 'list', 'post': 'create'}), name='vendor-list'),
    path('vendors/<int:vendor_id>/', views.VendorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='vendor-detail'),

    # Purchase Order Endpoints
    path('purchase-orders/', views.PurchaseOrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='purchase-order-list'),
    path('purchase-orders/<int:po_id>/', views.PurchaseOrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='purchase-order-detail'),

     # Performance Metrics 
    path('on-time-delivery-rate/', views.OnTimeDeliveryRateViewSet.as_view({'get': 'list'}), name='on-time-delivery'),
    path('quality-rating-average/', views.QualityRatingAverageViewSet.as_view({'get': 'list'}), name='quality-rating'),
    path('average-response-time/', views.AverageResponseTimeViewSet.as_view({'get': 'list'}), name='avg-response-time'),
    path('fulfilment-rate/', views.FulfilmentRateViewSet.as_view({'get': 'list'}), name='fulfilment-rate'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    # Acknowledgement 
    path('purchase-orders/<int:po_id>/acknowledge/', views.update_acknowledgment, name='update-acknowledgement'),
]

