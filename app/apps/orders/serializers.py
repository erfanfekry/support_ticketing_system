from rest_framework import serializers
from .models import *

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["name", "phone", "vehicle_number"]