from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True) # Phone number for receiving SMS
    last_seen = models.DateTimeField(null=True, blank=True) # Ticket's last seen 

    def __str__(self):
        return self.phone


class Driver(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=11)
    vehicle_plate_number = models.CharField(max_length=6) # Example: '123456'

    def __str__(self):
        return self.first_name + ' ' + self.last_name