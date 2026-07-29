from rest_framework.exceptions import ValidationError
from apps.orders.models import OrderStatus


class TicketValidator:

    @classmethod
    def validate_create(cls, order, data):
        cls._validate_order_has_no_ticket(order)

        if order.status == OrderStatus.DELIVERED:
            cls._validate_delivered(data)

        elif order.status == OrderStatus.SHIPPED:
            cls._validate_shipped(data)

        else:
            cls._validate_default(data)

    @staticmethod
    def _validate_order_has_no_ticket(order):
            if hasattr(order, "ticket"):
                raise ValidationError({"order_id": "A support ticket already exists for this order."})

    @staticmethod
    def _validate_delivered(data):
        if "description" not in data:
            raise ValidationError({"description": "This field is required."})
        if "image" not in data:
            raise ValidationError({"image": "This field is required."})

    @staticmethod
    def _validate_shipped(data):
        if not data.get('message'):
            raise ValidationError({"message": "This field is required."})

    @staticmethod
    def _validate_default(data):
        if not data.get('message'):
            raise ValidationError({"message": "This field is required."})
