from .selectors import get_order, get_ticket
from rest_framework.validators import ValidationError
from django.db import transaction
from .validators import TicketValidator
from .models import Ticket, TicketMessage, MessageAttachment
from apps.notifications.services import NotificationService

class TicketService:

    @classmethod
    @transaction.atomic
    def create_ticket(cls, *, user, validated_data):
        order = get_order(validated_data["order_id"], user)
        TicketValidator._validate_create(order, validated_data)
        ticket = cls._create_ticket(order)
        message = cls._create_message(ticket=ticket, user=user, validated_data=validated_data)
        cls._create_attachment(message=message,validated_data=validated_data)
        NotificationService.ticket_message_created(ticket=ticket, message=message, sender=user)

        return ticket

    @classmethod
    @transaction.atomic
    def add_message_to_existing_ticket(cls, *, ticket_id, user, validated_data):
        ticket = get_ticket(ticket_id, user)
        TicketValidator._validate_add_message(ticket, validated_data)
        message = cls._create_message(ticket=ticket, user=user, validated_data=validated_data)
        cls._create_attachment(message=message, validated_data=validated_data)
        NotificationService.ticket_message_created(ticket=ticket, message=message, sender=user)

        return ticket


    @staticmethod
    def _create_ticket(order):

        return Ticket.objects.create(order=order)

    @staticmethod
    def _create_message(*, ticket, user, validated_data):
        
        return TicketMessage.objects.create(ticket=ticket, sender=user, message=validated_data['text'])

    @staticmethod
    def _create_attachment(*, message, validated_data):
        image = validated_data.get("image")
        if not image:
            return
        MessageAttachment.objects.create(message=message, image=image)