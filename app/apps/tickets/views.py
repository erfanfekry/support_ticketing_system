from django.shortcuts import render
from .serializers import TicketCreateSerializer, TicketDetailSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.tickets.services import TicketService


class TicketCreateAPIView(generics.CreateAPIView):

    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = TicketService.create_ticket(user=request.user, validated_data=serializer.validated_data)
        response_serializer = TicketDetailSerializer(ticket)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)