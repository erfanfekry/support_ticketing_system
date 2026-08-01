from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.tickets.serializers import (TicketCreateSerializer,
                                      TicketListSerializer,
                                      TicketDetailSerializer,
                                      TicketReopenSerializer,
                                      AdminTicketDetailSerializer,
                                      AdminTicketReplySerializer)
from apps.tickets.selectors import get_customer_tickets, get_admin_ticket_list
from apps.tickets.services import TicketService
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter


@extend_schema_view(
    get=extend_schema(
        tags=["Customer Tickets"],
        summary="List customer tickets",
        description=(
            "Returns all support tickets belonging to the authenticated customer, "
            "ordered from newest to oldest."
        ),
        responses={
            200: TicketListSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
        },
    ),
    post=extend_schema(
        tags=["Customer Tickets"],
        summary="Create a support ticket",
        description=(
            "Creates a new support ticket for one of the authenticated customer's "
            "orders. Validation rules depend on the order status."
        ),
        request=TicketCreateSerializer,
        responses={
            201: TicketDetailSerializer,
            400: OpenApiResponse(description="Validation error."),
            401: OpenApiResponse(description="Authentication credentials were not provided."),
        },
    ),
)
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


@extend_schema(
    tags=["Customer Tickets"],
    summary="Retrieve ticket details",
    description=(
        "Returns the complete details of a support ticket belonging to the "
        "authenticated customer, including all messages, uploaded attachments, "
        "and driver information when applicable."
    ),
    responses={
        200: TicketDetailSerializer,
        401: OpenApiResponse(description="Authentication credentials were not provided."),
        404: OpenApiResponse(description="Ticket not found."),
    },
)
class CustomerTicketDetailAPIView(generics.RetrieveAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = TicketDetailSerializer
        def get_queryset(self):
            return get_customer_tickets(self.request.user)

@extend_schema(
    tags=["Customer Tickets"],
    summary="Add a message to a ticket",
    description=(
        "Adds a new message to an existing support ticket owned by the "
        "authenticated customer. An optional file attachment may be included. "
        "Submitting a message triggers the configured customer support notifications."
    ),
    request=TicketCreateSerializer,
    responses={
        201: TicketDetailSerializer,
        400: OpenApiResponse(description="Validation error."),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
        403: OpenApiResponse(description="You do not have permission to access this ticket."),
        404: OpenApiResponse(description="Ticket not found."),
    },
)
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


@extend_schema(
    tags=["Admin Tickets"],
    summary="List support tickets",
    description=(
        "Returns a list of all support tickets for administrators. "
        "Tickets are ordered from newest to oldest and include the data "
        "required for response-time monitoring, such as the last response "
        "timestamp or computed waiting state."
    ),
    parameters=[
        OpenApiParameter(
            name="delivered",
            type=bool,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Return only tickets associated with delivered orders.",
        ),
    ],
    responses={
        200: TicketListSerializer(many=True),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
        403: OpenApiResponse(description="Only administrators can access this endpoint."),
    },
)
class AdminTicketListAPIView(generics.ListAPIView):
        permission_classes = [IsAuthenticated, IsAdminUser]
        serializer_class = TicketListSerializer
        def get_queryset(self):
             return get_admin_ticket_list(self.request)


@extend_schema(
    tags=["Admin Tickets"],
    summary="Retrieve ticket details",
    description=(
        "Returns the complete details of a support ticket, including all "
        "messages, uploaded attachments, customer information, and the "
        "assigned driver's information (if available)."
    ),
    responses={
        200: AdminTicketDetailSerializer,
        401: OpenApiResponse(
            description="Authentication credentials were not provided."
        ),
        403: OpenApiResponse(
            description="Only administrators can access this endpoint."
        ),
        404: OpenApiResponse(
            description="Ticket not found."
        ),
    },
)
class AdminTicketDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AdminTicketDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_admin_ticket_list(self.request)
    

@extend_schema(
    tags=["Admin Tickets"],
    summary="Reply to a support ticket",
    description=(
        "Allows an administrator to post a reply to an existing support ticket. "
        "A reply may include a text message and an optional file attachment. "
        "Sending a reply triggers the configured customer notifications."
    ),
    request=AdminTicketReplySerializer,
    responses={
        201: TicketDetailSerializer,
        400: OpenApiResponse(description="Invalid request."),
        403: OpenApiResponse(description="Only administrators can access this endpoint."),
        404: OpenApiResponse(description="Ticket not found."),
    },
    examples=[
        OpenApiExample(
            "Reply",
            summary="Reply with attachment",
            value={
                "message": "Your issue has been resolved. Please verify and let us know if you need anything else."
            },
            request_only=True,
        )
    ],
)
class AdminTicketReplyAPIView(generics.GenericAPIView):
    serializer_class = AdminTicketReplySerializer
    permission_classes = [IsAdminUser]

    def post(self, request, ticket_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket_message = TicketService.reply(ticket_id=ticket_id, user=request.user, **serializer.validated_data)

        return Response(TicketDetailSerializer(ticket_message).data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Customer Tickets"],
    summary="Reopen a support ticket",
    description=(
        "Reopens a previously closed support ticket belonging to the "
        "authenticated customer. The ticket status will be changed back "
        "to open so further communication can continue."
    ),
    request=TicketReopenSerializer,
    responses={
        200: OpenApiResponse(
            description="Ticket reopened successfully."
        ),
        400: OpenApiResponse(
            description="Ticket cannot be reopened due to its current status."
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided."
        ),
        403: OpenApiResponse(
            description="You do not have permission to reopen this ticket."
        ),
        404: OpenApiResponse(
            description="Ticket not found."
        ),
    },
)
class CustomerTicketReopenAPIView(generics.GenericAPIView):
    serializer_class = TicketReopenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        TicketService.reopen(ticket_id=ticket_id, user=request.user)

        return Response({"detail": f"Ticket with id={ticket_id} was reopened successfully."}, status=status.HTTP_200_OK)