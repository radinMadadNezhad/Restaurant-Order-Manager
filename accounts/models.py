from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        ORDERER = 'ORDERER', 'Orderer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ORDERER,
    )
    LOCATION_CHOICES = (
        ('180 Queen', '180 Queen'),
        ('151 Yonge', '151 Yonge'),
        ('33 Yonge', '33 Yonge'),
    )
    location = models.CharField(max_length=100, blank=True, choices=LOCATION_CHOICES, help_text="Restaurant location")
    # New field to grant specific users permission to create shopping orders
    can_submit_shopping_orders = models.BooleanField(
        default=False, 
        help_text="Allow this user to create shopping orders regardless of their role"
    )

    class Meta:
        permissions = [
            ("submit_shopping_order", "Can submit shopping orders"),
            ("confirm_shopping_order", "Can confirm shopping orders"),
            ("view_shopping_order", "Can view shopping orders"),
            ("order_ingredients", "Can order ingredients"),
            ("view_ingredient_order", "Can view ingredient orders"),
            ("process_orders", "Can process orders"),
            ("admin_full_access", "Has full access to view and confirm everything"),
        ]

    def is_staff_role(self):
        return self.role == self.Role.STAFF

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def is_orderer(self):
        return self.role == self.Role.ORDERER

    def can_create_shopping_orders(self):
        # Users can create shopping orders if:
        # 1. They are staff or admin OR
        # 2. They have explicit permission via can_submit_shopping_orders field OR
        # 3. They have the submit_shopping_order permission
        is_staff = self.is_staff_role()
        is_admin = self.is_admin_role()
        has_perm = self.can_submit_shopping_orders
        has_permission = self.has_perm('accounts.submit_shopping_order')
        return is_staff or is_admin or has_perm or has_permission or self.is_orderer()

    def get_station_name(self):
        """Deprecated: station is now selected per order."""
        return None

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
