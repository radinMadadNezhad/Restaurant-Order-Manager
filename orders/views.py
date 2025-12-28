from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Ingredient,
    IngredientOrder,
    IngredientOrderItem,
    ShoppingOrder,
    ShoppingOrderItem,
    ShoppingIngredient,
    ContactMessage,
)
from .forms import (
    IngredientOrderForm,
    IngredientOrderItemForm,
    ShoppingOrderForm,
    ShoppingOrderItemForm,
    IngredientForm,
    ContactForm,
    ShoppingIngredientForm,
    IngredientManagementForm,
)
from .services import OrderService, ShoppingService


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )

            # Send email notification to admin
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                send_mail(
                    subject=f"New Contact Message: {msg.subject}",
                    message=(
                        f"From: {msg.name} <{msg.email}>\n\n"
                        f"Message:\n{msg.message}"
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost'),
                    recipient_list=[admin_email],
                    fail_silently=settings.DEBUG,
                )
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact_success.html')


# Management dashboard access control
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if getattr(user, 'is_admin_role', None) and user.is_admin_role():
            return view_func(request, *args, **kwargs)
        if user.has_perm('accounts.admin_full_access'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "You do not have access to Management.")
        return redirect('dashboard')
    return _wrapped


@admin_required
def management_home(request):
    from accounts.models import CustomUser
    from django.db.models import Count
    users_by_location = (
        CustomUser.objects.values('location').annotate(total=Count('id')).order_by('location')
    )
    orders_pending = IngredientOrder.objects.filter(status=IngredientOrder.Status.PENDING).count()
    orders_completed = IngredientOrder.objects.filter(status=IngredientOrder.Status.COMPLETED).count()
    recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
    return render(request, 'management/index.html', {
        'users_by_location': users_by_location,
        'orders_pending': orders_pending,
        'orders_completed': orders_completed,
        'recent_contacts': recent_contacts,
    })


# Users CRUD
from .forms import ManagementUserForm, StationForm, IngredientManagementForm, StationAssignmentForm


@admin_required
def management_users(request):
    from accounts.models import CustomUser
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'management/users_list.html', {'users': users})


@admin_required
def management_user_create(request):
    form = ManagementUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User created.')
        return redirect('management_users')
    return render(request, 'management/user_form.html', {'form': form, 'title': 'Create User'})


@admin_required
def management_user_edit(request, pk):
    from accounts.models import CustomUser
    user = get_object_or_404(CustomUser, pk=pk)
    form = ManagementUserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated.')
        return redirect('management_users')
    return render(request, 'management/user_form.html', {'form': form, 'title': 'Edit User'})


@admin_required
def management_user_delete(request, pk):
    from accounts.models import CustomUser
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('management_users')
    return render(request, 'management/confirm_delete.html', {'object': user, 'type': 'User'})


# Stations CRUD
@admin_required
def management_stations(request):
    from .models import Station
    stations = Station.objects.all()
    return render(request, 'management/stations_list.html', {'stations': stations})


@admin_required
def management_station_create(request):
    form = StationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Station created.')
        return redirect('management_stations')
    return render(request, 'management/station_form.html', {'form': form, 'title': 'Create Station'})


@admin_required
def management_station_edit(request, pk):
    from .models import Station
    station = get_object_or_404(Station, pk=pk)
    form = StationForm(request.POST or None, instance=station)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Station updated.')
        return redirect('management_stations')
    return render(request, 'management/station_form.html', {'form': form, 'title': 'Edit Station'})


@admin_required
def management_station_delete(request, pk):
    from .models import Station
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        station.delete()
        messages.success(request, 'Station deleted.')
        return redirect('management_stations')
    return render(request, 'management/confirm_delete.html', {'object': station, 'type': 'Station'})


# Ingredients CRUD
@admin_required
def management_ingredients(request):
    ingredients = Ingredient.objects.all().order_by('name')
    return render(request, 'management/ingredients_list.html', {'ingredients': ingredients})


@admin_required
def management_ingredient_create(request):
    form = IngredientManagementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ingredient created.')
        return redirect('management_ingredients')
    return render(request, 'management/ingredient_form.html', {'form': form, 'title': 'Create Ingredient'})


@admin_required
def management_ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    form = IngredientManagementForm(request.POST or None, instance=ingredient)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ingredient updated.')
        return redirect('management_ingredients')
    return render(request, 'management/ingredient_form.html', {'form': form, 'title': 'Edit Ingredient'})


@admin_required
def management_ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        ingredient.delete()
        messages.success(request, 'Ingredient deleted.')
        return redirect('management_ingredients')
    return render(request, 'management/confirm_delete.html', {'object': ingredient, 'type': 'Ingredient'})


# Station-Ingredient assignment
@admin_required
def management_station_ingredients(request):
    from .models import Station, StationIngredient
    form = StationAssignmentForm(request.POST or None)
    selected_station = None
    assigned_ids = []
    if request.method == 'POST' and form.is_valid():
        selected_station = form.cleaned_data['station']
        selected_ingredients = form.cleaned_data['ingredients']
        # Replace existing assignments
        StationIngredient.objects.filter(station=selected_station).delete()
        StationIngredient.objects.bulk_create([
            StationIngredient(station=selected_station, ingredient=ing)
            for ing in selected_ingredients
        ])
        messages.success(request, 'Assignments updated.')
    elif request.method == 'POST':
        messages.error(request, 'Please fix the errors below.')

    # If station selected (on GET with ?station=ID or after POST), preload selections
    if request.method == 'GET':
        station_id = request.GET.get('station')
        if station_id:
            try:
                selected_station = Station.objects.get(pk=station_id)
                form.fields['station'].initial = selected_station
            except Station.DoesNotExist:
                selected_station = None
    if selected_station:
        assigned_ids = list(StationIngredient.objects.filter(station=selected_station).values_list('ingredient_id', flat=True))
        form.fields['ingredients'].initial = assigned_ids

    return render(request, 'management/station_ingredients.html', {
        'form': form,
        'selected_station': selected_station,
    })

@login_required
def dashboard(request):
    # Ingredient orders visibility aligned with service permissions
    if OrderService.user_can_view_ingredient_order(request.user):
        ingredient_orders = (
            IngredientOrder.objects.select_related('orderer')
            .all()
            .order_by('-created_at')
        )
    else:
        ingredient_orders = IngredientOrder.objects.none()

    # Shopping orders visibility aligned with service permissions
    if OrderService.user_can_view_shopping_order(request.user):
        shopping_orders = (
            ShoppingOrder.objects.select_related('chef').all().order_by('-created_at')
        )
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
            order = OrderService.create_ingredient_order(
                user=request.user,
                notes=form.cleaned_data['notes'],
                items_data=items_data
            )
            # Attach station, location, and title
            order.station = form.cleaned_data['station']
            order.order_title = form.cleaned_data.get('order_title', '')
            # Use form location if provided, else fallback to user location
            order.location = form.cleaned_data.get('location') or request.user.location or ''
            order.save()
            
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
        'ingredients': ShoppingIngredient.objects.all()
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
    
    order = get_object_or_404(IngredientOrder, id=order_id)
    
    if request.method == 'POST':
        action = request.POST.get('action', 'process')
        OrderService.process_ingredient_order(order, action, user=request.user)
        
        if action == 'start':
            messages.info(request, 'Order marked as in progress.')
        elif action == 'complete':
            messages.success(request, 'Order marked as completed!')
        elif action == 'process':
            messages.success(request, 'Order marked as processed!')
        
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
            
            # Update additional fields manually before saving via service or after
            # Service updates notes and items. We need to update title, station, location.
            order.order_title = form.cleaned_data['order_title']
            order.station = form.cleaned_data['station']
            # Use form location if provided, else keep existing or user location
            location = form.cleaned_data.get('location')
            if location:
                order.location = location
            elif not order.location and request.user.location:
                order.location = request.user.location
            order.save()

            # Update order using service (handles notes and items)
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
        # Prefer StationIngredient mapping; fallback to legacy Ingredient.station
        if station != 'Unassigned':
            try:
                from .models import Station
                station_obj = Station.objects.get(name=station)
                form.fields['ingredient'].queryset = Ingredient.objects.filter(station_links__station=station_obj).distinct()
            except Station.DoesNotExist:
                form.fields['ingredient'].queryset = Ingredient.objects.filter(station=station)
    
    context = {
        'form': form,
        'order': order,
        'station': station
    }
    return render(request, 'orders/add_ingredient_to_order.html', context)


@admin_required
def ingredient_create_view(request):
    form = IngredientManagementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ingredient created.')
        return redirect('management_ingredients')
    return render(request, 'orders/ingredient_form_admin.html', {'form': form, 'title': 'Create Ingredient'})

@admin_required
def shopping_ingredient_create_view(request):
    form = ShoppingIngredientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Shopping Ingredient created.')
        return redirect('management_ingredients')
    return render(request, 'orders/shopping_ingredient_form_admin.html', {'form': form, 'title': 'Create Shopping Ingredient'})


@admin_required
def delete_ingredient_order(request, order_id):
    order = get_object_or_404(IngredientOrder, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Ingredient Order deleted successfully.')
        return redirect('dashboard')
    return render(request, 'orders/confirm_delete_order.html', {'order': order, 'type': 'Ingredient Order'})


@admin_required
def delete_shopping_order(request, order_id):
    order = get_object_or_404(ShoppingOrder, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Shopping Order deleted successfully.')
        return redirect('dashboard')
    return render(request, 'orders/confirm_delete_order.html', {'order': order, 'type': 'Shopping Order'})
