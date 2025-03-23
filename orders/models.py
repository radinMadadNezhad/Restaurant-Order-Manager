from django.db import models
from django.conf import settings
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    station = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class IngredientOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    orderer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredient_orders'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def get_items_by_station(self):
        """Group order items by the station of the user who added them"""
        result = {}
        
        for item in self.items.all():
            # Get the station name of the user who added the item
            if not item.added_by:
                # For legacy items with no added_by
                station_name = self.orderer.get_station_name()
            else:
                station_name = item.added_by.get_station_name()
            
            if station_name not in result:
                result[station_name] = []
            
            result[station_name].append(item)
            
        return result
        
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
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
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
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name}"
