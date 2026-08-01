from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from .models import Order
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    tags=["Orders"],
    summary="List orders",
    description=(
        "Returns a list of orders.\n\n"
        "- Customers receive only their own orders.\n"
        "- Administrators receive all orders."
    ),
    responses={
        200: OrderSerializer(many=True),
        401: OpenApiResponse(
            description="Authentication credentials were not provided."
        ),
    },
)
class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(customer=self.request.user)
        return orders
    