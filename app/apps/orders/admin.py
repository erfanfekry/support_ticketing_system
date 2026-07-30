from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import Order
from apps.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (('Additional Information', {'fields':('phone',)}),)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['customer', 'driver', 'status', 'delivered_at', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']