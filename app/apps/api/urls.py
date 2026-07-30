from django.urls import path
from apps.tickets.views import TicketCreateAPIView


app_name = 'api'

urlpatterns = [
    path( "tickets/", TicketCreateAPIView.as_view(), name="ticket-create"),
]