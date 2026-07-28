from django.db import models
from apps.users.models import User, Driver


class Status(models.TextChoices):
    WAITING_FOR_PAYMENT = "WPAY", "Waiting For Payment"
    PAID = "PAID", "Paid"
    PREPARATION = "PREP", "In Preparation"
    SHIPPED = "SHPD", "Shipped"
    DELIVERED = "DLVD", "Delivered"

class Order(models.Model):

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=30, choices=Status.choices)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['status'])
        ]