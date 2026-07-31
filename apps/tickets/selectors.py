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


def get_admin_ticket_list(request=None):
    admin_ticket_list = Ticket.objects.select_related("order", "order__customer").order_by("-created_at") \
    .annotate(last_message_time=Max("messages__created_at__time")) \
    .prefetch_related(Prefetch("messages", queryset=TicketMessage.objects.order_by("-created_at")))

    if request:
        if request.query_params.get("delivered") == "true":
         admin_ticket_list = admin_ticket_list.filter(order__status=OrderStatus.DELIVERED)

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
    .annotate(last_message_time=Max("messages__created_at__time")).filter(order__customer=user)

    return customer_tickets

def customer_get_ticket(ticket_id, user):
    ticket = get_object_or_404(Ticket.objects.select_related("order", "order__customer", "order__driver"),
                                    id=ticket_id,
                                    order__customer=user)
    return ticket

def admin_get_ticket(ticket_id, user):
    ticket = get_object_or_404(Ticket.objects.select_related("order", "order__customer", "order__driver"),
                                    id=ticket_id)
    return ticket