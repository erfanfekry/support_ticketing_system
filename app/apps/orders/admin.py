from django.contrib import admin
from .models import Order, Driver


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'driver', 'status', 'delivered_at', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['driver', 'status']


