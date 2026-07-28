from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True) # Phone number for receiving SMS
    last_seen = models.DateTimeField(null=True, blank=True) # Ticket's last seen 

    def __str__(self):
        return self.phone