from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from django.utils import timezone
from .models import (
    Ingredient,
    IngredientOrder,
    IngredientOrderItem,
    ShoppingOrder,
    ShoppingOrderItem
)
from .forms import (
    IngredientOrderForm,
    IngredientOrderItemForm,
    ShoppingOrderForm,
    ShoppingOrderItemForm,
    IngredientForm
)
from .services import OrderService, ShoppingService

@login_required
def dashboard(request):
    # Get ingredient orders - show all orders to all station users and staff
    if request.user.is_staff_role() or request.user.is_orderer() or request.user.is_salad_bar_role() or request.user.is_sandwich_role() or request.user.is_hot_station_role():
        # All these roles can see all orders - optimize with select_related
        ingredient_orders = IngredientOrder.objects.select_related('orderer').all().order_by('-created_at')
    else:
        ingredient_orders = IngredientOrder.objects.none()

    # Get shopping orders - only staff, admin, and users with permission can see these
    if request.user.is_staff_role() or request.user.is_admin_role() or request.user.can_create_shopping_orders():
        shopping_orders = ShoppingOrder.objects.select_related('chef').all().order_by('-created_at')
    else:
        shopping_orders = ShoppingOrder.objects.none()

    # Simple context without complex processing
    context = {
        'ingredient_orders': ingredient_orders,
        'shopping_orders': shopping_orders,
    }
    return render(request, 'orders/dashboard.html', context)

@login_required
def create_ingredient_order(request):
    if not OrderService.user_can_create_ingredient_order(request.user):
        messages.error(request, "You don't have permission to create ingredient orders.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IngredientOrderForm(request.POST)
        if form.is_valid():
            # Prepare items data from POST request
            items_data = []
            ingredient_ids = request.POST.getlist('ingredient')
            quantities = request.POST.getlist('quantity')
            
            for ingredient_id, quantity in zip(ingredient_ids, quantities):
                if ingredient_id and quantity:
                    items_data.append({
                        'ingredient_id': ingredient_id,
                        'quantity': quantity
                    })
            
            # Create order using service
            OrderService.create_ingredient_order(
                user=request.user,
                notes=form.cleaned_data['notes'],
                items_data=items_data
            )
            
            messages.success(request, 'Ingredient order submitted successfully!')
            return redirect('dashboard')
    else:
        form = IngredientOrderForm()
    
    context = {
        'form': form,
        'item_form': IngredientOrderItemForm(),
        'ingredients': Ingredient.objects.all()
    }
    return render(request, 'orders/create_ingredient_order.html', context)

@login_required
def create_shopping_order(request):
    # Debug print to help diagnose permission issues
    print(f"User: {request.user.username}, Can create orders: {request.user.can_create_shopping_orders()}")
    
    if not ShoppingService.user_can_create_shopping_order(request.user):
        messages.error(request, "You don't have permission to create shopping orders.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ShoppingOrderForm(request.POST)
        if form.is_valid():
            # Prepare items data from POST request
            items_data = []
            ingredient_ids = request.POST.getlist('ingredient')
            quantities = request.POST.getlist('quantity')
            notes_list = request.POST.getlist('notes')
            
            for ingredient_id, quantity, notes in zip(ingredient_ids, quantities, notes_list):
                if ingredient_id and quantity:
                    items_data.append({
                        'ingredient_id': ingredient_id,
                        'quantity': quantity,
                        'notes': notes
                    })
            
            # Create order using service
            ShoppingService.create_shopping_order(
                user=request.user,
                notes=form.cleaned_data['notes'],
                items_data=items_data
            )
            
            messages.success(request, 'Shopping order submitted successfully!')
            return redirect('dashboard')
    else:
        form = ShoppingOrderForm()
    
    context = {
        'form': form,
        'item_form': ShoppingOrderItemForm(),
        'ingredients': Ingredient.objects.all()
    }
    return render(request, 'orders/create_shopping_order.html', context)

@login_required
def confirm_shopping_order(request, order_id):
    if not OrderService.user_can_confirm_shopping_order(request.user):
        messages.error(request, "You don't have permission to confirm shopping orders.")
        return redirect('dashboard')
    
    order = get_object_or_404(ShoppingOrder, id=order_id, status='SUBMITTED')
    
    if request.method == 'POST':
        ShoppingService.confirm_shopping_order(order, request.user)
        messages.success(request, 'Shopping order confirmed successfully!')
        return redirect('dashboard')
    
    return render(request, 'orders/confirm_shopping_order.html', {'order': order})

@login_required
def process_ingredient_order(request, order_id):
    if not OrderService.user_can_process_ingredient_order(request.user):
        messages.error(request, "You don't have permission to process ingredient orders.")
        return redirect('dashboard')
    
    order = get_object_or_404(IngredientOrder, id=order_id, status='PENDING')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        OrderService.process_ingredient_order(order, action)
        
        if action == 'start':
            messages.info(request, 'Order marked as in progress.')
        elif action == 'complete':
            messages.success(request, 'Order marked as completed!')
        
        return redirect('dashboard')
    
    return render(request, 'orders/process_ingredient_order.html', {'order': order})

@login_required
def view_order_details(request, order_id, order_type):
    if order_type == 'ingredient':
        order = get_object_or_404(IngredientOrder, id=order_id)
        # Check permissions
        if not OrderService.user_can_view_ingredient_order(request.user):
            messages.error(request, "You don't have permission to view this order.")
            return redirect('dashboard')
        
        # Now all users get items grouped by station
        context = {
            'order': order,
            'items_by_station': order.get_items_by_station()
        }
        
        template = 'orders/ingredient_order_details.html'
    else:  # shopping
        order = get_object_or_404(ShoppingOrder, id=order_id)
        if not OrderService.user_can_view_shopping_order(request.user):
            messages.error(request, "You don't have permission to view this order.")
            return redirect('dashboard')
        context = {'order': order}
        template = 'orders/shopping_order_details.html'
    
    return render(request, template, context)

@login_required
def complete_shopping_order(request, order_id):
    order = get_object_or_404(ShoppingOrder, id=order_id)
    
    if not OrderService.user_can_view_shopping_order(request.user):
        messages.error(request, "You don't have permission to complete this order.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        if order.status != 'CONFIRMED':
            messages.error(request, "Only confirmed orders can be marked as complete.")
            return redirect('view_order_details', order_type='shopping', order_id=order.id)
        
        ShoppingService.complete_shopping_order(order)
        messages.success(request, f"Shopping Order #{order.id} has been marked as complete.")
    
    return redirect('dashboard')

@login_required
def edit_ingredient_order(request, order_id):
    order = get_object_or_404(IngredientOrder, id=order_id, status='PENDING')
    
    # Check if user has permission to edit this order
    if not OrderService.user_can_edit_ingredient_order(request.user, order):
        messages.error(request, "You don't have permission to edit this order.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IngredientOrderForm(request.POST, instance=order)
        if form.is_valid():
            # Prepare items data from POST request
            items_data = []
            ingredient_ids = request.POST.getlist('ingredient')
            quantities = request.POST.getlist('quantity')
            
            for ingredient_id, quantity in zip(ingredient_ids, quantities):
                if ingredient_id and quantity:
                    items_data.append({
                        'ingredient_id': ingredient_id,
                        'quantity': quantity
                    })
            
            # Update order using service
            OrderService.update_ingredient_order(
                order=order,
                notes=form.cleaned_data['notes'],
                items_data=items_data,
                user=request.user
            )
            
            messages.success(request, 'Order updated successfully!')
            return redirect('dashboard')
    else:
        form = IngredientOrderForm(instance=order)
    
    # Get only items added by this user
    items = order.items.filter(added_by=request.user)
    
    context = {
        'form': form,
        'item_form': IngredientOrderItemForm(),
        'ingredients': Ingredient.objects.all(),
        'order': order,
        'items': items
    }
    return render(request, 'orders/edit_ingredient_order.html', context)

@login_required
def ingredient_order_details(request, order_id):
    order = get_object_or_404(IngredientOrder, id=order_id)
    
    # Check if user has permission to view this order
    if not (request.user.is_staff_role or order.created_by == request.user):
        messages.error(request, "You don't have permission to view this order.")
        return redirect('dashboard')
    
    # For staff users, group items by station
    items_by_station = {}
    if request.user.is_staff_role:
        for item in order.items.all():
            station = item.ingredient.station
            if station not in items_by_station:
                items_by_station[station] = []
            items_by_station[station].append({
                'ingredient': item.ingredient,
                'quantity': item.quantity,
                'unit': item.ingredient.unit,
                'order_id': item.order.id
            })
    
    context = {
        'order': order,
        'items_by_station': items_by_station
    }
    return render(request, 'orders/ingredient_order_details.html', context)

@login_required
def edit_ingredient_order_item(request, order_id, item_id):
    order = get_object_or_404(IngredientOrder, id=order_id)
    item = get_object_or_404(IngredientOrderItem, id=item_id, order=order)
    
    # Check if user has permission to edit this item
    if not OrderService.user_can_edit_ingredient_order(request.user, order):
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('dashboard')
    
    # Only the user who added the item or staff can edit it
    if not (request.user.is_staff_role() or request.user == item.added_by):
        messages.error(request, "You can only edit items you added to the order.")
        return redirect('view_order_details', order_type='ingredient', order_id=order_id)
    
    if request.method == 'POST':
        form = IngredientOrderItemForm(request.POST, instance=item)
        if form.is_valid():
            OrderService.update_order_item(
                item=item,
                ingredient_id=form.cleaned_data['ingredient'].id,
                quantity=form.cleaned_data['quantity']
            )
            messages.success(request, 'Item updated successfully.')
            return redirect('view_order_details', order_type='ingredient', order_id=order_id)
    else:
        form = IngredientOrderItemForm(instance=item)
    
    context = {
        'form': form,
        'order': order,
        'item': item
    }
    return render(request, 'orders/edit_ingredient_order_item.html', context)

@login_required
def add_ingredient_to_order(request, order_id, station):
    order = get_object_or_404(IngredientOrder, id=order_id)
    
    # Check if user has permission to add items to this order
    if not OrderService.user_can_edit_ingredient_order(request.user, order):
        messages.error(request, "You don't have permission to add items to this order.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IngredientOrderItemForm(request.POST)
        if form.is_valid():
            OrderService.add_item_to_order(
                order=order,
                ingredient_id=form.cleaned_data['ingredient'].id,
                quantity=form.cleaned_data['quantity'],
                user=request.user
            )
            messages.success(request, 'Ingredient added successfully.')
            return redirect('view_order_details', order_type='ingredient', order_id=order_id)
    else:
        form = IngredientOrderItemForm()
        if station != 'Unassigned':
            form.fields['ingredient'].queryset = Ingredient.objects.filter(station=station)
    
    context = {
        'form': form,
        'order': order,
        'station': station
    }
    return render(request, 'orders/add_ingredient_to_order.html', context)
