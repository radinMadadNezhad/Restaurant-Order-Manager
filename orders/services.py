from django.utils import timezone
from django.db import transaction

class OrderService:
    """Service for handling business logic related to orders"""
    
    @staticmethod
    def user_can_create_ingredient_order(user):
        """Check if user has permission to create ingredient orders"""
        return user.is_orderer() or user.has_perm('accounts.order_ingredients')
    
    @staticmethod
    def user_can_create_shopping_order(user):
        """Check if user has permission to create shopping orders"""
        return user.can_create_shopping_orders()
    
    @staticmethod
    def user_can_confirm_shopping_order(user):
        """Check if user has permission to confirm shopping orders"""
        return user.is_admin_role() or user.has_perm('accounts.confirm_shopping_order')
    
    @staticmethod
    def user_can_process_ingredient_order(user):
        """Check if user has permission to process ingredient orders"""
        return user.is_staff_role() or user.has_perm('accounts.process_orders')
    
    @staticmethod
    def user_can_edit_ingredient_order(user, order):
        """Check if user has permission to edit an ingredient order"""
        # Allow orderers and those with the explicit permission to edit
        return user.is_orderer() or user.has_perm('accounts.order_ingredients')
    
    @staticmethod
    def user_can_view_ingredient_order(user):
        """Check if user has permission to view ingredient orders"""
        return (
            user.is_staff_role() or user.is_orderer() or
            user.has_perm('accounts.view_ingredient_order') or
            user.has_perm('accounts.admin_full_access')
        )
    
    @staticmethod
    def user_can_view_shopping_order(user):
        """Check if user has permission to view shopping orders"""
        return (user.is_staff_role() or user.is_admin_role() or 
                user.can_create_shopping_orders() or 
                user.has_perm('accounts.view_shopping_order') or
                user.has_perm('accounts.admin_full_access'))
    
    @staticmethod
    def create_ingredient_order(user, notes, items_data):
        """Create a new ingredient order with items"""
        from .models import IngredientOrder, IngredientOrderItem
        
        with transaction.atomic():
            order = IngredientOrder.objects.create(
                orderer=user,
                notes=notes,
                status=IngredientOrder.Status.PENDING
            )
            
            # Create order items
            for item_data in items_data:
                # Store the user's station with each item for grouping
                IngredientOrderItem.objects.create(
                    order=order,
                    ingredient_id=item_data['ingredient_id'],
                    quantity=item_data['quantity'],
                    added_by=user  # Track who added this item
                )
                
            return order
    
    @staticmethod
    def update_ingredient_order(order, notes, items_data, user):
        """Update an existing ingredient order with new items"""
        from .models import IngredientOrderItem
        
        with transaction.atomic():
            # Update order details
            order.notes = notes
            order.save()
            
            # Delete existing items added by this user
            order.items.filter(added_by=user).delete()
            
            # Create new items with user attribution
            for item_data in items_data:
                IngredientOrderItem.objects.create(
                    order=order,
                    ingredient_id=item_data['ingredient_id'],
                    quantity=item_data['quantity'],
                    added_by=user  # Track who added this item
                )
            
            return order
    
    @staticmethod
    def process_ingredient_order(order, action):
        """Process an ingredient order based on the action"""
        if action == 'start':
            order.status = order.Status.IN_PROGRESS
        elif action == 'complete':
            order.status = order.Status.COMPLETED
        order.save()
        return order
    
    @staticmethod
    def add_item_to_order(order, ingredient_id, quantity, user):
        """Add a new item to an existing order"""
        from .models import IngredientOrderItem
        
        item = IngredientOrderItem.objects.create(
            order=order,
            ingredient_id=ingredient_id,
            quantity=quantity,
            added_by=user  # Track who added this item
        )
        return item
    
    @staticmethod
    def update_order_item(item, ingredient_id, quantity):
        """Update an existing order item"""
        from .models import Ingredient
        
        item.ingredient_id = ingredient_id
        item.quantity = quantity
        item.save()
        
        return item


class ShoppingService:
    """Service for handling business logic related to shopping"""
    
    @staticmethod
    def user_can_create_shopping_order(user):
        """Check if user has permission to create shopping orders"""
        return user.can_create_shopping_orders()
    
    @staticmethod
    def create_shopping_order(user, notes, items_data):
        """Create a new shopping order with items"""
        from .models import ShoppingOrder, ShoppingOrderItem
        
        with transaction.atomic():
            order = ShoppingOrder.objects.create(
                chef=user,
                notes=notes,
                status=ShoppingOrder.Status.SUBMITTED
            )
            
            # Create order items
            for item_data in items_data:
                ShoppingOrderItem.objects.create(
                    order=order,
                    ingredient_id=item_data['ingredient_id'],
                    quantity=item_data['quantity'],
                    notes=item_data.get('notes', '')
                )
                
            return order
    
    @staticmethod
    def confirm_shopping_order(order, user):
        """Confirm a shopping order"""
        order.status = order.Status.CONFIRMED
        order.confirmed_by = user
        order.confirmed_at = timezone.now()
        order.save()
        return order
    
    @staticmethod
    def complete_shopping_order(order):
        """Mark a shopping order as complete"""
        order.status = order.Status.COMPLETED
        order.save()
        return order 
