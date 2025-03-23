from django import forms
from .models import (
    Ingredient,
    IngredientOrder,
    IngredientOrderItem,
    ShoppingOrder,
    ShoppingOrderItem
)

class IngredientOrderForm(forms.ModelForm):
    class Meta:
        model = IngredientOrder
        fields = ['notes']

class IngredientOrderItemForm(forms.ModelForm):
    class Meta:
        model = IngredientOrderItem
        fields = ['ingredient', 'quantity']

class ShoppingOrderForm(forms.ModelForm):
    class Meta:
        model = ShoppingOrder
        fields = ['notes']

class ShoppingOrderItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingOrderItem
        fields = ['ingredient', 'quantity']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit'] 