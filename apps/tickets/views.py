from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.tickets.serializers import (TicketCreateSerializer,
                                      TicketListSerializer,
                                      TicketDetailSerializer,
                                      AdminTicketDetailSerializer,
                                      AdminTicketReplySerializer)
from apps.tickets.selectors import get_customer_tickets, get_admin_ticket_list
from apps.tickets.services import TicketService
from drf_spectacular.utils import extend_schema, OpenApiResponse


class CustomerTicketListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TicketListSerializer
        elif self.request.method == "POST":
            return TicketCreateSerializer

    def get_queryset(self):
        return get_customer_tickets(self.request.user)
        
    def get(self, request):
        """
        List all tickets belonging to the authenticated customer.
        """
        queryset = self.get_queryset()
        serilizer = self.get_serializer(queryset, many=True)
        return Response(serilizer.data)

    def post(self, request):
        """
        Create a new support ticket.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = TicketService.create_ticket(user=request.user, validated_data=serializer.validated_data)
        response_serializer = TicketDetailSerializer(ticket)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CustomerTicketDetailAPIView(generics.RetrieveAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = TicketDetailSerializer
        def get_queryset(self):
            return get_customer_tickets(self.request.user)

class CustomerTicketMessageAPIView(generics.CreateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = TicketCreateSerializer

        def post(self, request, ticket_id):
                """
                Create a new message for an existing ticket.
                """
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                ticket = TicketService.add_message_to_existing_ticket(user=request.user,
                                                                      ticket_id=ticket_id,
                                                                      validated_data=serializer.validated_data)
                response_serializer = TicketDetailSerializer(ticket)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class AdminTicketListAPIView(generics.ListAPIView):
        permission_classes = [IsAuthenticated, IsAdminUser]
        serializer_class = TicketListSerializer
        def get_queryset(self):
             return get_admin_ticket_list(self.request)


@extend_schema(
    tags=["Admin Tickets"],
    summary="Ticket details",
    description="Retrieve a ticket including driver information and messages.",
    responses={
        200: AdminTicketDetailSerializer,
    },
)      
class AdminTicketDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AdminTicketDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_admin_ticket_list(self.request)
    

class AdminTicketReplyAPIView(generics.GenericAPIView):
    serializer_class = AdminTicketReplySerializer
    permission_classes = [IsAdminUser]

    def post(self, request, ticket_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket_message = TicketService.reply(ticket_id=ticket_id, user=request.user, **serializer.validated_data)

        return Response(TicketDetailSerializer(ticket_message).data, status=status.HTTP_201_CREATED)