from django.urls import path
from apps.tickets.views import CustomerTicketListCreateAPIView, \
                               CustomerTicketDetailAPIView, \
                               CustomerTicketMessageAPIView, \
                               AdminTicketListAPIView, \
                               AdminTicketDetailAPIView, \
                               AdminTicketReplyAPIView
                               

                               
from apps.orders.views import OrderListAPIView



app_name = 'api'

urlpatterns = [
    path( "orders/", OrderListAPIView.as_view(), name="order-list"),
    path( "tickets/", CustomerTicketListCreateAPIView.as_view(), name="customer-ticket-list-create"),
    path( "tickets/<int:pk>/", CustomerTicketDetailAPIView.as_view(), name="customer-ticket-detail"),
    path( "tickets/<int:ticket_id>/messages/", CustomerTicketMessageAPIView.as_view(), name="customer-ticket-message"),
    path( "admin/tickets/", AdminTicketListAPIView.as_view(), name="admin-ticket-list"),
    path( "admin/tickets/<int:pk>/", AdminTicketDetailAPIView.as_view(), name="admin-ticket-detail"),
    path( "admin/tickets/<int:ticket_id>/reply/", AdminTicketReplyAPIView.as_view(), name="admin-ticket-reply"),



]