from django.contrib import admin
from .models import Ticket, TicketMessage, MessageAttachment


class MessageInline(admin.TabularInline):
    model=TicketMessage
    extra = 0

class MessageAttachmentline(admin.TabularInline):
    model=MessageAttachment
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'order', 'status', 'created_at', 'closed_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    inlines = [MessageInline]

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket_id', 'ticket', 'sender', 'message', 'created_at']
    list_filter = ['sender', 'created_at']
    inlines = [MessageAttachmentline]

