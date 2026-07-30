from django.urls import path
from apps.tickets.views import CustomerTicketListCreateAPIView, CustomerTicketDetailAPIView
from apps.orders.views import OrderListAPIView



app_name = 'api'

urlpatterns = [
    path( "orders/", OrderListAPIView.as_view(), name="order-list"),
    path( "tickets/", CustomerTicketListCreateAPIView.as_view(), name="customer-ticket-list-create"),
    path( "tickets/<int:pk>/", CustomerTicketDetailAPIView.as_view(), name="customer-ticket-detail"),


]