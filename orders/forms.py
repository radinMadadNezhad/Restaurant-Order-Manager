from django import forms
from decimal import Decimal
from .models import (
    Ingredient,
    IngredientOrder,
    IngredientOrderItem,
    ShoppingOrder,
    ShoppingOrderItem,
    ShoppingIngredient,
    Station,
)

class IngredientOrderForm(forms.ModelForm):
    station = forms.ModelChoiceField(queryset=Station.objects.all(), required=True)

    class Meta:
        model = IngredientOrder
        fields = ['order_title', 'station', 'location', 'notes']

class IngredientOrderItemForm(forms.ModelForm):
    quantity = forms.DecimalField(min_value=Decimal('0.01'))
    class Meta:
        model = IngredientOrderItem
        fields = ['ingredient', 'quantity']

class ShoppingOrderForm(forms.ModelForm):
    class Meta:
        model = ShoppingOrder
        fields = ['notes']

class ShoppingOrderItemForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    quantity = forms.DecimalField(min_value=Decimal('0.01'))
    
    class Meta:
        model = ShoppingOrderItem
        fields = ['ingredient', 'quantity', 'notes']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))


# Management Dashboard Forms
from accounts.models import CustomUser


class ManagementUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep unchanged")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'location', 'can_submit_shopping_orders', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name']


class IngredientManagementForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']


class ShoppingIngredientForm(forms.ModelForm):
    class Meta:
        model = ShoppingIngredient
        fields = ['name', 'unit', 'description']


class StationAssignmentForm(forms.Form):
    station = forms.ModelChoiceField(queryset=Station.objects.all())
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'size': 12}))
