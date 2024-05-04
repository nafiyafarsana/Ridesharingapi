from django.urls import path
from .views import RegisterDriver, RideListCreateAPIView, RideDetailAPIView, AcceptRideView, StartRideView, CompleteRideView, CancelRideView, RideLocationView, track_location, request_ride,accept_ride

urlpatterns = [
    path('register-driver/', RegisterDriver.as_view(), name='register-driver'),
    path('rides/', RideListCreateAPIView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideDetailAPIView.as_view(), name='ride-detail'),
    path('rides/<int:pk>/accept/',AcceptRideView.as_view(), name='accept_ride'),
    path('rides/<int:pk>/start/', StartRideView.as_view(), name='start_ride'),
    path('rides/<int:pk>/complete/', CompleteRideView.as_view(), name='complete_ride'),
    path('rides/<int:pk>/cancel/', CancelRideView.as_view(), name='cancel_ride'),
    path('rid/<int:pk>/', RideLocationView.as_view(), name='ride-details'),
    path('track-location/<int:ride_id>/', track_location, name='track-location'),
    path('request-ride/', request_ride, name='request_ride'),
    path('accept-ride/', accept_ride, name='accept_ride'),
]