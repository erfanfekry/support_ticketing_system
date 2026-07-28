from django.db import models
from apps.users.models import User
from apps.orders.models import Order


class Status(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    InProgress = 'INPR', 'In progress'
    CLOSED = 'CLSD', 'Closed'

class Ticket(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="ticket")
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
            indexes = [
                models.Index(fields=['status']),
                models.Index(fields=['created_at'])
            ]
