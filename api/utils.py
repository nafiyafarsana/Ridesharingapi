from geopy.distance import geodesic
from .models import Driver
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

def match_ride_to_driver(ride_request):
    available_drivers = Driver.objects.filter(is_available=True)
    print(available_drivers)

    for driver in available_drivers:
        distance = calculate_distance((ride_request.pickup_lat, ride_request.pickup_lng), 
                                      (driver.location_lat, driver.location_lng))
        # You can add more logic to calculate score and choose the best driver
        driver.score = distance
    
    best_driver = min(available_drivers, key=lambda driver: driver.score)
    print(best_driver)
    
    return best_driver