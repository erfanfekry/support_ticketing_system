from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User, Driver


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (('Additional Information', {'fields':('phone',)}),)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'vehicle_plate_number']
    list_filter = ['phone', 'vehicle_plate_number']

