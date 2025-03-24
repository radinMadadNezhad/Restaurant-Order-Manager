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