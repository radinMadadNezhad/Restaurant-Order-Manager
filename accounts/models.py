from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        SALAD_BAR = 'SALAD_BAR', 'Salad Bar'
        SANDWICH = 'SANDWICH', 'Sandwich'
        HOT_STATION = 'HOT_STATION', 'Hot Station'
        ORDERER = 'ORDERER', 'Orderer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ORDERER,
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Restaurant location"
    )

    def is_staff_role(self):
        return self.role == self.Role.STAFF

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def is_orderer(self):
        return self.role == self.Role.ORDERER

    def is_salad_bar_role(self):
        return self.role == self.Role.SALAD_BAR

    def is_sandwich_role(self):
        return self.role == self.Role.SANDWICH

    def is_hot_station_role(self):
        return self.role == self.Role.HOT_STATION

    def get_station_name(self):
        """Return the station name based on the user's role"""
        if self.is_salad_bar_role():
            return 'Salad Bar Station'
        elif self.is_sandwich_role():
            return 'Sandwich Station'
        elif self.is_hot_station_role():
            return 'Hot Station'
        return None

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
