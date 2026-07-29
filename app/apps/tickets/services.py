from .selectors import *
from rest_framework.validators import ValidationError

class TicketService:

    @classmethod
    def create_ticket(cls, *, user, validated_data):
        order = get_order( validated_data["order_id"], user)

    @staticmethod
    def ticket_exists(order):
        if hasattr(order, "ticket"):
            raise ValidationError("Ticket already exists.")