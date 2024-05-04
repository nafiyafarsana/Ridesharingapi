from rest_framework import serializers
from .models import Ride,RideRequest,Driver

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = ['user_name', 'pickup_lat', 'pickup_lng', 'destination_lat', 'destination_lng']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'email', 'phone_number', 'car_model', 'license_plate', 'location_lat', 'location_lng', 'is_available']
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False},
            'car_model': {'required': False},
            'license_plate': {'required': False},
        }