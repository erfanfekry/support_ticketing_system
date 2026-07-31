from rest_framework import serializers
from .models import *
from apps.orders.serializers import *
from datetime import timedelta
from django.utils import timezone


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
    waiting_state = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "order_id", "customer", "status", "created_at", "last_message_time", "waiting_state"]

    def get_last_message_time(self, obj):
        return obj.last_message_time.strftime("%H:%M:%S")

    def get_waiting_state(self, ticket):
        messages = ticket.messages.all()

        if not messages:
            return "answered"

        last_message = messages[0]

        if last_message.sender.is_staff:
            return "answered"

        waiting_time = timezone.now() - last_message.created_at

        if waiting_time >= timedelta(hours=72):
            return "waiting_72h"

        if waiting_time >= timedelta(hours=24):
            return "waiting_24h"

        return "waiting"
    

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
        fields = ["id", "status", "order_id", "created_at", "driver", "messages"]

class CreateTicketMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)

class AdminTicketDetailSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True)
    driver = DriverSerializer(source="order.driver")

    class Meta:
        model = Ticket
        fields = ["id", "status", "order_id", "created_at", "driver", "messages"]

class AdminTicketReplySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=5000)
    attachment = serializers.FileField(required=False)