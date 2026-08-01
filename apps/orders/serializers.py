from rest_framework import serializers
from .models import Order
from apps.users.models import Driver
from apps.users.serializers import UserSerializer


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "first_name",  "last_name", "phone", "vehicle_plate_number"]


class OrderSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    customer = UserSerializer()
    class Meta:
            model = Order
            fields = ["id", "customer", "driver", "status", "delivered_at", "created_at"]

