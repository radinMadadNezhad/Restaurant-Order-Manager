import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_management.settings')
django.setup()

from orders.models import Ingredient

# List of ingredients with their units
ingredients_data = [
    # Vegetables
    {'name': 'Mushrooms', 'unit': 'kg'},
    {'name': 'Cucumber', 'unit': 'kg'},
    {'name': 'Tomatoes', 'unit': 'kg'},
    {'name': 'Lettuce', 'unit': 'heads'},
    {'name': 'Bell Peppers', 'unit': 'kg'},
    {'name': 'Onions', 'unit': 'kg'},
    {'name': 'Carrots', 'unit': 'kg'},
    
    # Proteins
    {'name': 'Chicken Breast', 'unit': 'kg'},
    {'name': 'Tuna', 'unit': 'cans'},
    {'name': 'Ham', 'unit': 'kg'},
    {'name': 'Turkey', 'unit': 'kg'},
    
    # Dairy and Condiments
    {'name': 'Cheddar Cheese', 'unit': 'kg'},
    {'name': 'Mozzarella', 'unit': 'kg'},
    {'name': 'Ranch Dressing', 'unit': 'liters'},
    {'name': 'Mayonnaise', 'unit': 'liters'},
    {'name': 'Mustard', 'unit': 'liters'},
    {'name': 'Olive Oil', 'unit': 'liters'},
    
    # Bread
    {'name': 'White Bread', 'unit': 'loaves'},
    {'name': 'Whole Wheat Bread', 'unit': 'loaves'},
    {'name': 'Baguette', 'unit': 'pieces'},
]

def create_ingredients():
    for ingredient_data in ingredients_data:
        Ingredient.objects.get_or_create(
            name=ingredient_data['name'],
            defaults={
                'unit': ingredient_data['unit']
            }
        )
        print(f"Added/Updated ingredient: {ingredient_data['name']}")

if __name__ == '__main__':
    print("Creating ingredients...")
    create_ingredients()
    print("Done!") 