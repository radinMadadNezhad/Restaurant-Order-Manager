from django import template

register = template.Library()

@register.filter
def can_create_shopping_orders(user):
    """Template filter to check if a user can create shopping orders"""
    return user.can_create_shopping_orders()

@register.filter
def is_admin_role(user):
    """Template filter to check if a user has admin role"""
    return user.is_admin_role()

@register.filter
def is_staff_role(user):
    """Template filter to check if a user has staff role"""
    return user.is_staff_role()

@register.filter
def is_orderer(user):
    """Template filter to check if a user is orderer"""
    return user.is_orderer()

@register.filter
def is_salad_bar_role(user):
    """Template filter to check if a user has salad bar role"""
    return user.is_salad_bar_role()

@register.filter 
def is_sandwich_role(user):
    """Template filter to check if a user has sandwich role"""
    return user.is_sandwich_role()

@register.filter
def is_hot_station_role(user):
    """Template filter to check if a user has hot station role"""
    return user.is_hot_station_role()

# New permissions based template tags
@register.filter
def can_submit_shopping_order(user):
    """Check if user has permission to submit shopping orders"""
    return user.has_perm('accounts.submit_shopping_order') or user.can_create_shopping_orders()

@register.filter
def can_confirm_shopping_order(user):
    """Check if user has permission to confirm shopping orders"""
    return user.has_perm('accounts.confirm_shopping_order') or user.is_admin_role()

@register.filter
def can_view_shopping_order(user):
    """Check if user has permission to view shopping orders"""
    return (user.has_perm('accounts.view_shopping_order') or 
            user.has_perm('accounts.submit_shopping_order') or
            user.has_perm('accounts.confirm_shopping_order') or
            user.has_perm('accounts.admin_full_access') or
            user.can_create_shopping_orders())

@register.filter
def can_order_ingredients(user):
    """Check if user has permission to order ingredients"""
    return user.has_perm('accounts.order_ingredients') or user.is_orderer()

@register.filter
def can_view_ingredient_order(user):
    """Check if user has permission to view ingredient orders"""
    return (user.has_perm('accounts.view_ingredient_order') or
            user.has_perm('accounts.admin_full_access') or
            user.has_perm('accounts.order_ingredients') or
            user.is_orderer() or user.is_staff_role())

@register.filter
def can_process_orders(user):
    """Check if user has permission to process orders"""
    return user.has_perm('accounts.process_orders') or user.is_staff_role()

@register.filter
def has_admin_full_access(user):
    """Check if user has full admin access"""
    return user.has_perm('accounts.admin_full_access') or user.is_admin_role() 