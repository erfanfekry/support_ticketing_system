from rest_framework import serializers

class TicketCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    message = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)