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
    last_message_time = serializers.SerializerMethodField() # Will be defined in selectors.py ...
    unanswered_messages = serializers.SerializerMethodField() # Will be defined in selectors.py ...

    class Meta:
        model = Ticket
        fields = ["id", "order_id", "customer", "status", "created_at", "last_message_time", "unanswered_messages"]


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ["id", "image", "uploaded_at"]        