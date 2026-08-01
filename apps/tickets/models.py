from django.db import models
from apps.users.models import User
from apps.orders.models import Order


class TicketStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLSD', 'Closed'

class Ticket(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="ticket")
    status = models.CharField(max_length=4, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
            indexes = [
                models.Index(fields=['status']),
                models.Index(fields=['created_at'])
            ]
    def __str__(self):
         return f'Ticket of oreder id: {self.order.id}'

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class MessageAttachment(models.Model):
    message = models.ForeignKey(TicketMessage, on_delete=models.CASCADE, related_name="attachments")
    image = models.ImageField(upload_to="tickets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
