import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_management.settings')
django.setup()

from orders.models import ShoppingIngredient

def create_shopping_ingredients():
    ingredients_data = [
        {
            'name': 'Paper Towels',
            'unit': 'rolls',
            'description': 'For cleaning and wiping'
        },
        {
            'name': 'Dish Soap',
            'unit': 'bottles',
            'description': 'For washing dishes'
        },
        {
            'name': 'Hand Soap',
            'unit': 'bottles',
            'description': 'For hand washing'
        },
        {
            'name': 'Trash Bags',
            'unit': 'rolls',
            'description': 'For waste disposal'
        },
        {
            'name': 'Aluminum Foil',
            'unit': 'rolls',
            'description': 'For food storage and cooking'
        },
        {
            'name': 'Plastic Wrap',
            'unit': 'rolls',
            'description': 'For food storage'
        },
        {
            'name': 'Disposable Gloves',
            'unit': 'boxes',
            'description': 'For food handling'
        },
        {
            'name': 'Cleaning Sponges',
            'unit': 'packages',
            'description': 'For cleaning'
        }
    ]

    for ingredient_data in ingredients_data:
        ingredient, created = ShoppingIngredient.objects.get_or_create(
            name=ingredient_data['name'],
            defaults={
                'unit': ingredient_data['unit'],
                'description': ingredient_data['description']
            }
        )
        if created:
            print(f"Created shopping ingredient: {ingredient.name}")
        else:
            print(f"Shopping ingredient already exists: {ingredient.name}")

if __name__ == '__main__':
    create_shopping_ingredients() 