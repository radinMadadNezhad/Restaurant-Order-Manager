from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# Register the Permission model in the admin
admin.site.register(Permission)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Role and Restaurant'), {
            'fields': ('role', 'location'),
        }),
        (_('Legacy Permissions'), {
            'fields': ('can_submit_shopping_orders',),
            'description': 'Legacy permission fields that will be phased out in favor of Django permissions.',
        }),
        (_('Django Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Use these permissions for fine-grained control instead of role-based access.',
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 
                   'can_submit_shopping_orders', 'has_submit_shopping_permission')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 
                  'can_submit_shopping_orders', 'groups', 'user_permissions')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def has_submit_shopping_permission(self, obj):
        """Check if user has the submit_shopping_order permission"""
        return obj.has_perm('accounts.submit_shopping_order')
    has_submit_shopping_permission.boolean = True
    has_submit_shopping_permission.short_description = "Has Django Shopping Permission"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            # Only show the custom permissions from our app, not all Django permissions
            kwargs['queryset'] = Permission.objects.filter(content_type__app_label='accounts')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(CustomUser, CustomUserAdmin)
