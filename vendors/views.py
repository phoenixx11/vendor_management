from django.shortcuts import render
from rest_framework import viewsets , generics , serializers
from .models import Vendor, PurchaseOrder, PerformanceMetric
from .serializers import VendorSerializer, PurchaseOrderSerializer, PerformanceMetricSerializer , VendorPerformanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from django.http import JsonResponse

current_date_time = datetime.now()
PurchaseOrder.acknowledged_date = current_date_time

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve vendor performance data.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, pk=None):
        """
        Retrieves the performance data for a specific vendor (identified by primary key).
        """
        try:
            vendor = self.get_object()  # Retrieve vendor instance using generic lookup
            performance_data = {
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'avg_response_time': vendor.avg_response_time,
                'fulfillment_rate': vendor.fulfillment_rate,
            }
            serializer = self.get_serializer(performance_data)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response('Vendor not found with the provided ID.', status=status.HTTP_404_NOT_FOUND)

class OnTimeDeliveryRateViewSet(viewsets.ViewSet):
    """
    API endpoint to calculate on-time delivery rate.
    """

    def list(self, request):
        completed_orders = PurchaseOrder.objects.filter(status='completed')
        on_time_deliveries = sum(
            order.delivery_date <= order.acknowledged_date for order in completed_orders
        )
        delivery_rate = (on_time_deliveries / len(completed_orders)) * 100 if completed_orders else 0
        return Response({'on_time_delivery_rate': delivery_rate})

class QualityRatingAverageViewSet(viewsets.ViewSet):
    """
    API endpoint to calculate average quality rating.
    """

    def list(self, request):
        completed_orders = PurchaseOrder.objects.filter(status='completed')
        # ... ( logic to get quality ratings for completed orders)
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        return Response({'average_quality_rating': average_rating})

class AverageResponseTimeViewSet(viewsets.ViewSet):
    """
    API endpoint to calculate average response time.
    """

    def list(self, request):
        pos = PurchaseOrder.objects.all()
        average_response_time = sum(
            (order.acknowledged_date - order.issue_date).total_seconds() / len(pos)
            for order in pos
            if order.acknowledged_date
        )
        return Response({'average_response_time': average_response_time})

class FulfilmentRateViewSet(viewsets.ViewSet):
    """
    API endpoint to calculate fulfilment rate.
    """

    def list(self, request):
        completed_orders = PurchaseOrder.objects.filter(status='completed')
        fulfilled_orders = len(completed_orders)
        total_orders = PurchaseOrder.objects.count()
        fulfilment_rate = (fulfilled_orders / total_orders) * 100 if total_orders else 0
        return Response({'fulfilment_rate': fulfilment_rate})


@api_view(['POST'])
def update_acknowledgment(request, po_id):
    """
    API endpoint to update acknowledgment for a purchase order.
    """

    try:
        PurchaseOrder = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    if PurchaseOrder.status != 'pending':
        return Response({'error': 'Purchase order status must be pending to acknowledge'}, status=status.HTTP_400_BAD_REQUEST)

    PurchaseOrder.acknowledged_date = datetime.datetime.now()
    PurchaseOrder.save()

    # Recalculate average response time here 

    return Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)


    
def update_acknowledgment(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    
    # Update acknowledgment date
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    
    # Trigger recalculation of avg_response_time
    purchase_order.calculate_avg_response_time()
    
    return JsonResponse({'message': 'Acknowledgment date updated successfully.'})