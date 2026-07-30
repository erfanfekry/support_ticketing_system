from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.tickets.serializers import TicketCreateSerializer, TicketListSerializer, TicketDetailSerializer
from apps.tickets.selectors import get_customer_tickets
from apps.tickets.services import TicketService
from .permissions import IsOwner


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
        response_serializer = self.get_serializer(ticket)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CustomerTicketDetailAPIView(generics.RetrieveAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = TicketDetailSerializer
        def get_queryset(self):
            return get_customer_tickets(self.request.user)

