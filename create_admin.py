import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_management.settings')
django.setup()

User = get_user_model()

def create_admin_user():
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_user(
            username='admin',
            password='admin',
            role=User.OWNER,  # Give owner role for maximum permissions
            is_staff=True,    # Give staff permissions
            is_superuser=True # Give superuser permissions
        )
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")

if __name__ == '__main__':
    create_admin_user() 