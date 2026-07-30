from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'order', 'status', 'created_at', 'closed_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
