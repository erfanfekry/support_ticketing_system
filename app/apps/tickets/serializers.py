from rest_framework import serializers
from .models import *


class TicketCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    message = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)


class TicketListSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id")
    customer = serializers.CharField(source="order.customer.username")
    last_message_time = serializers.SerializerMethodField()
    unanswered_messages = serializers.SerializerMethodField()

    class Meta:

        model = Ticket
        fields = ["id", "order_id", "customer", "status", "created_at", "last_message_time", "unanswered_messages"]