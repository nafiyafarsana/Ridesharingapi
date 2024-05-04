from django.contrib import admin
from .models import Ride,RideRequest,Driver

# Register your models here.
admin.site.register(Ride)
admin.site.register(RideRequest)
admin.site.register(Driver)