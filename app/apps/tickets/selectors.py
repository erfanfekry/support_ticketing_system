from django.db.models import Prefetch
from apps.tickets.models import *


def get_ticket_detail(ticket_id):
    ticket = Ticket.objects.select_related("order", "order__driver", "order__customer") \
    .prefetch_related(Prefetch("messages", queryset=TicketMessage.objects.prefetch_related("attachments"))) \
    .get(id=ticket_id)

    return ticket

    
def get_user_tickets(user):
    tickets = Ticket.objects.filter(order__customer=user).select_related("order").order_by("-created_at")

    return tickets