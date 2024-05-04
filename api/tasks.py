import os
import requests
from celery import shared_task
from .models import Ride

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', "AIzaSyDXvVBJCZiJtQ4cV5XeOPmXC5S9yO7uGHI")

@shared_task
def update_ride_location(ride_id):
    try:
        # Get the ride object from the database
        ride = Ride.objects.get(pk=ride_id)

        # Call the GPS service's API to retrieve the current location
        response = requests.get(f'https://maps.googleapis.com/maps/api/geolocation?key={API_KEY}')

        # Parse the response and update the ride's location
        if response.status_code == 200:
            location_data = response.json()
            latitude = location_data['location']['lat']
            longitude = location_data['location']['lng']
            ride.current_latitude = latitude
            ride.current_longitude = longitude
            ride.save()
            return 'Location updated successfully'
        else:
            return f'Failed to update location: {response.status_code}'
    except Ride.DoesNotExist:
        return 'Ride not found'
    except Exception as e:
        return f'An error occurred: {str(e)}'