from rest_framework.exceptions import ValidationError
from apps.orders.models import OrderStatus
from apps.tickets.models import TicketStatus
import os


class TicketValidator:

    @classmethod
    def _validate_create(cls, order, data):
        cls._validate_order_has_no_ticket(order)
        status = order.status

        if status == OrderStatus.DELIVERED:
            cls._validate_delivered(data)

        elif status == OrderStatus.SHIPPED:
            cls._validate_shipped(data)

        else:
            cls._validate_default(data)

        data["text"] = (data.get("message") or data.get("description"))


        

    @staticmethod
    def _validate_order_has_no_ticket(order):
            if hasattr(order, "ticket"):
                raise ValidationError({"order_id": "A support ticket already exists for this order."})

    @classmethod
    def _validate_delivered(cls, data, ticket=None):
        if not data.get("description") and not ticket:
            raise ValidationError({"description": "This field is required."})
        if not data.get("image") and not ticket:
            raise ValidationError({"image": "This field is required."})
        image = data.get("image")
        if image:
            cls._validate_image(image)

    @staticmethod
    def _validate_shipped(data):
        if data.get("image"):
            raise ValidationError({"image": "Images are not allowed for this order status."})

        if data.get("description"):
            raise ValidationError({"description": "Description is not allowed for this order status."})

        if not data.get("message"):
            raise ValidationError({"message": "This field is required."})
        
    @staticmethod
    def _validate_default(data):
        if data.get("image"):
                    raise ValidationError({"image": "Images are not allowed for this order status."})
        
        if data.get("description"):
            raise ValidationError({"description": "Description is not allowed for this order status."})

        if not data.get("message"):
            raise ValidationError({"message": "This field is required."})


    @staticmethod
    def _validate_image(image):
        MAX_IMAGE_SIZE = 5 * 1024 * 1024
        ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

        if image.size > MAX_IMAGE_SIZE:
            raise ValidationError({
                "image": "Image size must not exceed 5 MB."
            })

        extension = os.path.splitext(image.name)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError({"image": ("Only JPG, JPEG and PNG images are allowed.")})

    @classmethod
    def _validate_add_message(cls, ticket, data):
        cls._validate_ticket_is_open(ticket)

        status = ticket.order.status

        if status == OrderStatus.DELIVERED:
            cls._validate_delivered(data, ticket)
        
        elif status == OrderStatus.SHIPPED:
             cls._validate_shipped(data)
        
        else:
                cls._validate_default(data)
        
        data["text"] = (data.get("message")or data.get("description"))
        


    @staticmethod
    def _validate_ticket_is_open(ticket):
        if ticket.status == TicketStatus.CLOSED:
            raise ValidationError({"ticket": "Cannot add messages to a closed ticket."})
