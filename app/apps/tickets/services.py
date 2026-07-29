from .selectors import *
from rest_framework.validators import ValidationError
from django.db import transaction
from .validators import *


class NotificationService: # will be defined
    @classmethod
    def ticket_message_created(cls, ticket, message):
        pass


class TicketService:

    @classmethod
    @transaction.atomic
    def create_ticket(cls, *, user, validated_data):

        order = get_order(validated_data["order_id"], user)

        TicketValidator.validate_create(order, validated_data)

        ticket = cls._create_ticket(order)

        message = cls._create_first_message(ticket=ticket, user=user, validated_data=validated_data)

        cls._create_attachment_if_exists(message=message,validated_data=validated_data)

        NotificationService.ticket_message_created(ticket=ticket, message=message)

        return ticket

    @staticmethod
    def _create_ticket(order):

        return Ticket.objects.create(order=order, status=TicketStatus.OPEN)

    @staticmethod
    def _create_first_message(*, ticket, user, validated_data):
        text = validated_data.get("message") or validated_data.get("description")

        return TicketMessage.objects.create(ticket=ticket, sender=user, message=text,)

    @staticmethod
    def _create_attachment_if_exists(*, message, validated_data):
        image = validated_data.get("image")
        if not image:
            return
        MessageAttachment.objects.create(message=message, image=image)