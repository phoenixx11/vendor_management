from django.db import models
from django.utils import timezone
from jsonfield import JSONField 
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vendor_id = models.CharField(max_length=100)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg  = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfilment_rate = models.FloatField(blank=True, null=True) 
    

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_id = models.CharField(max_length=1000)
    items = models.JSONField(default=list)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    acknowledgement_date = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class PerformanceMetric(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)  
    fulfilment_rate = models.FloatField(blank=True, null=True)  
    quality_rating_avg  = models.FloatField(blank=True, null=True) 
    average_response_time = models.FloatField(blank=True, null=True)  

def __str__(self):
        return f"PurchaseOrder {self.pk}"

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        # Count the number of completed purchase orders delivered on or before the delivery date
        total_completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
        on_time_delivered_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='completed',
            delivery_date__lte=models.F('actual_delivery_date')  # Assuming actual_delivery_date is available
        ).count()
        
        # Calculate the on-time delivery rate
        if total_completed_orders > 0:
            on_time_delivery_rate = (on_time_delivered_orders / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0
        
        # Update the on_time_delivery_rate field in the Vendor model
        instance.vendor.on_time_delivery_rate = on_time_delivery_rate
        instance.vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        # Calculate the average quality rating for the vendor
        avg_quality_rating = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').aggregate(
            average_quality_rating=models.Avg('quality_rating')
        )['average_quality_rating']
        
        # Update the quality_rating_avg field in the Vendor model
        instance.vendor.quality_rating_avg = avg_quality_rating
        instance.vendor.save()



@receiver(post_save, sender=PurchaseOrder)
def update_avg_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgement_date and instance.issue_date:
        # Calculate time difference in seconds
        time_difference = (instance.acknowledgement_date - instance.issue_date).total_seconds()
        
        # Update the average response time for the vendor
        avg_response_time = PurchaseOrder.objects.filter(vendor=instance.vendor).aggregate(
            average_response_time=models.Avg(models.F('acknowledgement_date') - models.F('issue_date'))
        )['average_response_time']
        
        # Update the avg_response_time field in the PurchaseOrder model
        instance.vendor.avg_response_time = avg_response_time
        instance.vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    # Calculate the fulfillment rate
    total_orders = PurchaseOrder.objects.count()
    fulfilled_orders = PurchaseOrder.objects.filter(status='completed').count()
    
    if total_orders > 0:
        fulfillment_rate = (fulfilled_orders / total_orders) * 100
    else:
        fulfillment_rate = 0
    
    # Update the fulfillment rate field in the PurchaseOrder model
    PurchaseOrder.objects.update(fulfillment_rate=fulfillment_rate)