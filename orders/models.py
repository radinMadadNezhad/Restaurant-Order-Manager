from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    station = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StationIngredient(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='station_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='station_links')

    class Meta:
        unique_together = ('station', 'ingredient')

    def __str__(self):
        return f"{self.station.name} + {self.ingredient.name}"

class IngredientOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        PROCESSED = 'PROCESSED', 'Processed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    orderer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredient_orders'
    )
    # New fields: link order to a station and tag with user's location
    station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    location = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="processed_orders"
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    order_title = models.CharField(max_length=100, blank=True, default='')
    notes = models.TextField(blank=True, null=True)

    def get_items_by_station(self):
        """Return items grouped under the selected station (compat with legacy)."""
        station_name = self.station.name if self.station else 'Unassigned'
        return {station_name: list(self.items.all())}
        
    def __str__(self):
        return f"Ingredient Order #{self.id} - {self.orderer.username}"

class IngredientOrderItem(models.Model):
    order = models.ForeignKey(
        IngredientOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_items',
        null=True
    )

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name}"

class ShoppingOrder(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    chef = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_orders_created'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shopping_orders_confirmed'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Shopping Order #{self.id} - {self.status}"

class ShoppingIngredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ['name']

class ShoppingOrderItem(models.Model):
    order = models.ForeignKey('ShoppingOrder', related_name='items', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(ShoppingIngredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.name} <{self.email}>"
