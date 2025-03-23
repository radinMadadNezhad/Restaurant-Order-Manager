import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import CustomUser

def create_users():
    # Create users with different roles
    users_data = [
        {
            'username': 'radin',  # Admin/Owner - already exists, just update role
            'password': 'admin123',
            'role': CustomUser.Role.OWNER,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'staff_user',
            'password': 'staff123',
            'role': CustomUser.Role.STAFF,
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'shopping_assistant',
            'password': 'shop123',
            'role': CustomUser.Role.SHOPPING_ASSISTANT,
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'salad_bar',
            'password': 'salad123',
            'role': CustomUser.Role.SALAD_BAR,
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'sandwich',
            'password': 'sand123',
            'role': CustomUser.Role.SANDWICH,
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'hot_station',
            'password': 'hot123',
            'role': CustomUser.Role.HOT_STATION,
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'cold_station',
            'password': 'cold123',
            'role': CustomUser.Role.COLD_STATION,
            'is_staff': False,
            'is_superuser': False
        }
    ]

    User = get_user_model()

    for user_data in users_data:
        username = user_data['username']
        try:
            user = User.objects.get(username=username)
            # Update existing user
            user.role = user_data['role']
            user.is_staff = user_data['is_staff']
            user.is_superuser = user_data['is_superuser']
            user.set_password(user_data['password'])
            user.save()
            print(f"Updated user: {username}")
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                password=user_data['password'],
                role=user_data['role'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser']
            )
            print(f"Created user: {username}")

if __name__ == '__main__':
    print("Creating users...")
    create_users()
    print("Done!") 