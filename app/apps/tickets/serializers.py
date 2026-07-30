from rest_framework import serializers
from .models import *
from apps.orders.serializers import *


class TicketCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    message = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)


class TicketListSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id")
    customer = serializers.CharField(source="order.customer.username")
    last_message_time = serializers.SerializerMethodField(read_only=True)
    # unanswered_messages = serializers.SerializerMethodField() # Will be defined in ...

    class Meta:
        model = Ticket
        fields = ["id", "order_id", "customer", "status", "created_at", "last_message_time"]

    def get_last_message_time(self, obj):
        return obj.last_message_time.strftime("%H:%M:%S")
    

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ["id", "image", "uploaded_at"]        


class TicketMessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True,read_only=True)
    sender = serializers.CharField(source="sender.username")
    class Meta:
        model = TicketMessage
        fields = ["id", "sender", "message", "created_at", "attachments"]


class TicketDetailSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True, read_only=True)
    driver = DriverSerializer(source="order.driver", read_only=True)
    class Meta:
        model = Ticket
        fields = ["id", "status", "created_at", "messages", "driver"]