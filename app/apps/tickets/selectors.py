from django.db.models import Prefetch
from apps.orders.models import Order, OrderStatus
from apps.tickets.models import Ticket,TicketMessage
from django.shortcuts import get_object_or_404
from django.db.models import Max, Count, Q



def get_ticket_detail(ticket_id):
    client_ticket_list = Ticket.objects.select_related("order", "order__driver", "order__customer") \
    .prefetch_related(Prefetch("messages", queryset=TicketMessage.objects.prefetch_related("attachments"))) \
    .get(id=ticket_id)

    return client_ticket_list

    
def get_user_tickets(user):
    tickets = Ticket.objects.filter(order__customer=user).select_related("order").order_by("-created_at")

    return tickets


def get_admin_ticket_list():
    admin_ticket_list = Ticket.objects.select_related("order", "order__customer").order_by("-created_at")

    return admin_ticket_list


def get_delivered_tickets():
    delivered_tickets = Ticket.objects.filter(order__status=OrderStatus.DELIVERED) \
    .select_related("order","order__customer")

    return delivered_tickets



def get_order(order_id, user):
    order = get_object_or_404(Order.objects.select_related("driver"), id=order_id, customer=user)

    return order

def get_customer_tickets(user):
    customer_tickets = Ticket.objects.select_related("order", "order__customer") \
    .annotate(last_message_time=Max("messages__created_at"))

    return customer_tickets
