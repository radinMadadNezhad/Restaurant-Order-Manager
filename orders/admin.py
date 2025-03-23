from django.contrib import admin
from .models import Ingredient, IngredientOrder, IngredientOrderItem, ShoppingOrder, ShoppingOrderItem, ShoppingIngredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)

class ShoppingIngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'description')
    search_fields = ('name', 'description')

class IngredientOrderItemInline(admin.TabularInline):
    model = IngredientOrderItem
    extra = 1

class ShoppingOrderItemInline(admin.TabularInline):
    model = ShoppingOrderItem
    extra = 1

class IngredientOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderer', 'status', 'created_at')
    list_filter = ('status', 'orderer__role')
    inlines = [IngredientOrderItemInline]
    readonly_fields = ('created_at', 'updated_at')

class ShoppingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'chef', 'status', 'created_at')
    list_filter = ('status', 'chef__role')
    inlines = [ShoppingOrderItemInline]
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShoppingIngredient, ShoppingIngredientAdmin)
admin.site.register(IngredientOrder, IngredientOrderAdmin)
admin.site.register(ShoppingOrder, ShoppingOrderAdmin)
