from django.db import models
from django.utils import timezone
# from users.models import User
# Create your models here

class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    rider = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ride #{self.pk}'
    
class Driver(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    car_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class RideRequest(models.Model):
    user_name = models.CharField(max_length=100)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    destination_lat = models.FloatField()
    destination_lng = models.FloatField()
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user_name