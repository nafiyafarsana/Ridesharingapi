from django.shortcuts import render
import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Ride,RideRequest,Driver
from .serializer import RideSerializer,RideRequestSerializer,DriverSerializer
from .tasks import update_ride_location
from .utils import match_ride_to_driver



# Create your views here.

class RegisterDriver(APIView):
    def post(self, request, format=None):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideListCreateAPIView(APIView):
    def get(self, request):
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ride = self.get_object(pk)
        serializer = RideSerializer(ride)
        return Response(serializer.data)
    
class AcceptRideView(APIView):
    def put(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
            if ride.status != 'REQUESTED':
                return Response({'error': 'Ride cannot be accepted as it is not in the requested state.'}, status=status.HTTP_400_BAD_REQUEST)
            
            ride.status = 'ACCEPTED'
            ride.save()
            serializer = RideSerializer(ride)
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class StartRideView(APIView):
    def put(self, request, pk):
        ride = Ride.objects.get(pk=pk)
        ride.status = 'ONGOING'
        ride.save()
        serializer = RideSerializer(ride)
        return Response(serializer.data)

class CompleteRideView(APIView):
    def put(self, request, pk):
        ride = Ride.objects.get(pk=pk)
        ride.status = 'COMPLETED'
        ride.save()
        serializer = RideSerializer(ride)
        return Response(serializer.data)

class CancelRideView(APIView):
    def put(self, request, pk):
        ride = Ride.objects.get(pk=pk)
        ride.status = 'CANCELLED'
        ride.save()
        serializer = RideSerializer(ride)
        return Response(serializer.data)
    
class RideLocationView(APIView):
    def get(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
            serializer = RideSerializer(ride)
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found.'}, status=status.HTTP_404_NOT_FOUND)
        
def track_location(request, ride_id):
    # Trigger the Celery task asynchronously
    update_ride_location.delay(ride_id)
    return HttpResponse('Location update task queued successfully')


@api_view(['POST'])
def request_ride(request):
    serializer = RideRequestSerializer(data=request.data)
    if serializer.is_valid():
        ride_request = serializer.save()
        driver = match_ride_to_driver(ride_request)
        ride_request.driver = driver
        ride_request.save()
        return Response({'message': 'Ride request sent successfully'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def accept_ride(request):
    driver_id = request.data.get('driver_id')
    ride_request_id = request.data.get('ride_request_id')
    try:
        ride_request = RideRequest.objects.get(pk=ride_request_id)
        driver = Driver.objects.get(pk=driver_id)
        ride_request.driver = driver
        ride_request.save()
        driver.is_available = False
        driver.save()
        return Response({'message': 'Ride request accepted successfully'}, status=200)
    except (RideRequest.DoesNotExist, Driver.DoesNotExist):
        return Response({'message': 'Invalid driver or ride request'}, status=400)